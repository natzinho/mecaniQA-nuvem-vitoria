"""Testes deterministas da aquisicao e da classificacao de resultados."""

import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from prometheus_client import REGISTRY

SOURCE = Path(__file__).resolve().parents[1] / "iot-simulator" / "simulator.py"
SPEC = importlib.util.spec_from_file_location("simulator", SOURCE)
simulator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(simulator)


class SimulatorTests(unittest.TestCase):
    def value(self, name, sensor, result=None):
        labels = {"sensor_id": sensor}
        if result is not None:
            labels["result"] = result
        return REGISTRY.get_sample_value(name, labels)

    def test_success_generates_three_readings_and_one_operation(self):
        sensor = "test-success"
        simulator.sample_sensors([sensor], error_probability=0)
        self.assertEqual(self.value("iot_sensor_operations_total", sensor, "success"), 1)
        self.assertEqual(self.value("iot_sensor_operations_total", sensor, "error"), 0)
        self.assertEqual(self.value("iot_sensor_readings_total", sensor), 3)
        for name, low, high in [
            ("iot_engine_temperature_celsius", 70, 110),
            ("iot_oil_pressure_bar", 1.5, 5.5),
            ("iot_vibration_meters_per_second_squared", 0.1, 4),
        ]:
            self.assertTrue(low <= self.value(name, sensor) <= high)

    def test_failure_keeps_last_successful_reading_and_timestamp(self):
        sensor = "test-retained"
        simulator.sample_sensors([sensor], error_probability=0)
        old_time = self.value("iot_sensor_last_update_timestamp_seconds", sensor)
        old_temperature = self.value("iot_engine_temperature_celsius", sensor)
        simulator.sample_sensors([sensor], error_probability=1)
        self.assertEqual(self.value("iot_sensor_operations_total", sensor, "error"), 1)
        self.assertEqual(self.value("iot_sensor_operations_total", sensor, "success"), 1)
        self.assertEqual(self.value("iot_sensor_readings_total", sensor), 3)
        self.assertEqual(self.value("iot_sensor_last_update_timestamp_seconds", sensor), old_time)
        self.assertEqual(self.value("iot_engine_temperature_celsius", sensor), old_temperature)

    def test_first_failure_publishes_both_outcomes_without_fake_readings(self):
        sensor = "test-first-failure"
        simulator.sample_sensors([sensor], error_probability=1)
        self.assertEqual(self.value("iot_sensor_operations_total", sensor, "error"), 1)
        self.assertEqual(self.value("iot_sensor_operations_total", sensor, "success"), 0)
        self.assertIsNone(self.value("iot_engine_temperature_celsius", sensor))

    def test_counter_counts_one_attempt_per_equipment_per_cycle(self):
        sensor = "test-attempts"
        for probability in [0, 1, 0, 1]:
            simulator.sample_sensors([sensor], error_probability=probability)
        self.assertEqual(self.value("iot_sensor_operations_total", sensor, "success"), 2)
        self.assertEqual(self.value("iot_sensor_operations_total", sensor, "error"), 2)
        self.assertEqual(self.value("iot_sensor_readings_total", sensor), 6)

    def test_config_probability_boundaries_and_invalid_values(self):
        for raw, expected in [("0", 0), ("1", 1), ("0.1", 0.1)]:
            with patch.dict(os.environ, {"SIMULATION_ERROR_PROBABILITY": raw}, clear=True):
                self.assertEqual(simulator.read_config(), (8000, 5, 3, expected))
        for value in ["-0.1", "1.1", "nan", "inf", "abc"]:
            with self.subTest(value=value):
                with patch.dict(os.environ, {"SIMULATION_ERROR_PROBABILITY": value}, clear=True):
                    with self.assertRaises(ValueError):
                        simulator.read_config()


if __name__ == "__main__":
    unittest.main()
