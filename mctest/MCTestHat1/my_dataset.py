import datasets

"""
Custom data loading script, made by following:
https://huggingface.co/docs/datasets/dataset_script
"""

class HeathersMCTest(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        HeathersMCTestConfig(
            name="heather",
            features = ["story", "story_id", "question", "question_id",
                "q_type", "choices", "answer", "text_answer", "label"],
            path_to_dir = "/Users/AZ01DN/postdoc/mcdata/MCTest",
            split = "mc160.dev",
            ),
    ]


class HeathersMCTestConfig(datasets.BuilderConfig):

    def __init__(self, features, path_to_dir, split, label_classes=("A", "B", "C", "D"), **kwargs):
        """BuilderConfig for MCTEST.

        Args:
        features: *list[string]*, list of the features that will appear in the
            feature dict. Should not include "label".
        path_to_dir: *string*, ...
        split: *string*, ...
        label_classes: *list[string]*, the list of classes for the label if the
            label is present as a string. Non-string labels will be cast to either
            'False' or 'True'.
        **kwargs: keyword arguments forwarded to super.
        """

        super().__init__(version=datasets.Version("1.0.2"), ** kwargs)
        self.featres = features
        self.path_to_dir = path_to_dir
        self.split = split
        self.label_classes = label_classes

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "story": datasets.Value("string"),
                    "story_id": datasets.Value("string"),
                    "question_id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "q_type": datasets.Value("string"),
                    "choices": datasets.Sequence("string"),
                    "answer": datasets.Value("string"),
                    "text_answer": datasets.Value("string"),
                    "label": datasets.Value("string"),

                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://creolenlp.github.io/mctest/",
            citation=_CITATION,
        )

