import unittest
from unittest.mock import mock_open, patch
import json
from rpG import save, load

# test_rpG.py



class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        self.status = {"gesundheit": 80, "movementkram": 90, "hunger": 10}
        self.inventar = {"ar15": (1, "ar", 200, 500, 2, 100, 5.56, 500), "stick": (20,)}
        self.inventarQa = {"ar15": 1, "stick": 2, "club": 0}
        self.stats = {"strength": 1, "speed": 2, "endurance": 3, "intelligence": 4, "charisma": 5, "maxHP": 99}
        self.data = {
            "status": self.status,
            "inventar": self.inventar,
            "inventarQa": self.inventarQa,
            "stats": self.stats
        }

    @patch("builtins.open", new_callable=mock_open)
    def test_save(self, mock_file):
        save(self.status, self.inventar, self.inventarQa, self.stats)
        mock_file.assert_called_once_with("save.json", "w", encoding="utf-8")
        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        saved_data = json.loads(written)
        self.assertEqual(saved_data["status"], self.status)
        self.assertEqual(saved_data["inventar"], self.inventar)
        self.assertEqual(saved_data["inventarQa"], self.inventarQa)
        self.assertEqual(saved_data["stats"], self.stats)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "status": {"gesundheit": 80, "movementkram": 90, "hunger": 10},
        "inventar": {"ar15": [1, "ar", 200, 500, 2, 100, 5.56, 500], "stick": [20]},
        "inventarQa": {"ar15": 1, "stick": 2, "club": 0},
        "stats": {"strength": 1, "speed": 2, "endurance": 3, "intelligence": 4, "charisma": 5, "maxHP": 99}
    }))
    @patch("rpG.input", return_value="testuser")
    def test_load(self, mock_input, mock_file):
        # Patch main to prevent running the main loop
        with patch("rpG.main", return_value=None):
            status, inventar, inventarQa, stats = load()
        self.assertEqual(status["gesundheit"], 80)
        self.assertEqual(inventar["ar15"][0], 1)
        self.assertEqual(inventarQa["stick"], 2)
        self.assertEqual(stats["maxHP"], 99)

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("rpG.input", return_value="testuser")
    def test_load_file_not_found(self, mock_input, mock_file):
        with patch("rpG.main", return_value=("main_called",)):
            result = load()
        self.assertEqual(result, ("main_called",))

if __name__ == "__main__":
    unittest.main()