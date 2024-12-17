import unittest
import json
import logging
import os
import sys
from unittest.mock import patch, MagicMock
from concurrent.futures import ProcessPoolExecutor

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Update sys.path to ensure modeling.py is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

try:
    from modeling import process_articles, categorize_terms, process_single_paper
    logging.debug("Successfully imported `process_articles`, `process_single_paper` and `categorize_terms`.")
except ImportError as e:
    logging.error("Failed to import `modeling`: %s", e)
    raise

class TestTopicModeling(unittest.TestCase):
    def setUp(self):
        """
        Set up mock test data dynamically.
        """
        logging.debug("Setting up mock test data and paths.")
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.output_file = os.path.join(base_path, "output_1.json")

        # Mock input data
        self.mock_input_data = {
            "papers": [
                {
                    "paper_name": "test_paper_1",
                    "cleaned_text": "PTSD is associated with DNA methylation and generational trauma.",
                    "term_counts": {
                        "mental health terms": {"PTSD": 2, "anxiety": 1},
                        "epigenetic terms": {"DNA methylation": 3},
                        "ethnographic terms": {"African descent": 1}
                    }
                }
            ]
        }

        self.expected_output_data = {
            "papers": [
                {
                    "paper_id": 1,
                    "categorized_counts": {
                        "Mental Health": {"General": {"PTSD": 2, "anxiety": 1}},
                        "Epigenetic": {"General": {"DNA methylation": 3}},
                        "Socioeconomic": {},
                        "Ethnographic": {"African descent": {"African descent": 1}}
                    }
                }
            ]
        }

        # Save input JSON file
        self.input_file = os.path.join(base_path, "test_input.json")
        with open(self.input_file, "w") as infile:
            json.dump(self.mock_input_data, infile)

    def tearDown(self):
        """
        Clean up generated files.
        """
        logging.debug("Cleaning up generated files.")
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.input_file):
            os.remove(self.input_file)

    def test_process_articles(self):
        """
        Test processing articles and verify output against expected JSON.
        """
        logging.debug("Running `test_process_articles`.")
        
        # Define mock output for a single paper
        mock_processed_paper = {
            "paper_id": 1,
            "categorized_counts": {
                "Mental Health": {"General": {"PTSD": 2, "anxiety": 1}},
                "Epigenetic": {"General": {"DNA methylation": 3}},
                "Socioeconomic": {},
                "Ethnographic": {"African descent": {"African descent": 1}}
            }
        }

        # Patch process_single_paper to return the mock output
        with patch("modeling.process_single_paper", return_value=mock_processed_paper):
            process_articles(self.input_file, self.output_file)

        # Verify output file exists
        self.assertTrue(os.path.exists(self.output_file), "Output file was not created.")

        # Load and compare the output JSON
        with open(self.output_file, "r") as outfile:
            output_data = json.load(outfile)

        expected_output = {"papers": [mock_processed_paper]}

        self.assertEqual(
            output_data,
            expected_output,
            "The output JSON does not match the expected JSON."
        )


    def test_categorize_terms(self):
        """
        Test categorization logic for terms.
        """
        logging.debug("Running `test_categorize_terms`.")
        term_counts = {
            "PTSD": 2,
            "anxiety": 1,
            "DNA methylation": 3,
            "African-American": 1
        }

        mental_health_categories = ["PTSD", "anxiety", "depression"]
        epigenetic_categories = ["DNA methylation", "BDNF", "FKBP5"]
        ethnographic_categories = {"African descent": ["African-American"]}

        # Call categorize_terms
        result = categorize_terms(term_counts, {
            "Mental Health": mental_health_categories,
            "Epigenetic": epigenetic_categories,
            "Ethnographic": ethnographic_categories
        })

        # Print result for debugging
        logging.debug(f"Categorized result: {result}")
        print("Categorized result:", result)

        # Assertions updated to match subcategory behavior
        self.assertEqual(result["Mental Health"]["PTSD"], 2)
        self.assertEqual(result["Epigenetic"]["DNA methylation"], 3)
        self.assertEqual(result["African descent"]["African-American"], 1)


if __name__ == "__main__":
    unittest.main()
