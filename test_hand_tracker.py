import unittest

from hand_tracker import build_parser, parse_source, validate_args

class SourceParsingTests(unittest.TestCase):
    def test_integer_source_is_camera_index(self):
        self.assertEqual(parse_source("0"), 0)

    def test_non_integer_source_is_video_path(self):
        self.assertEqual(parse_source("clips/demo video.mp4"), "clips/demo video.mp4")


class ArgumentValidationTests(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_defaults_are_usable(self):
        args = self.parser.parse_args([])
        validate_args(args, self.parser)
        self.assertEqual(args.max_hands, 2)
        self.assertEqual(args.source, "0")

    def test_no_preview_requires_output(self):
        args = self.parser.parse_args(["--no-preview"])
        with self.assertRaises(SystemExit):
            validate_args(args, self.parser)

    def test_out_of_range_confidence_is_rejected(self):
        args = self.parser.parse_args(["--detection-confidence", "1.5"])
        with self.assertRaises(SystemExit):
            validate_args(args, self.parser)

if __name__ == "__main__":
    unittest.main()
