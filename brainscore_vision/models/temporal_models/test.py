import os

from brainio.stimuli import StimulusSet
import brainscore_vision
from brainscore_vision import load_model
from brainscore_vision.model_helpers.activations.temporal.utils import switch_inferencer
from brainscore_vision.model_helpers.activations.temporal.core import CausalInferencer


HOME_DIR = brainscore_vision.__path__[0]
TEST_DIR = os.path.join(HOME_DIR, "../tests/test_model_helpers/temporal")


def _build_stimulus_set():
    video_names=["dots1.mp4", "dots2.mp4"]
    stimulus_set = StimulusSet([{'stimulus_id': video_name, 'some_meta': video_name[::-1]}
                                for video_name in video_names])
    stimulus_set.stimulus_paths = {video_name: os.path.join(TEST_DIR, video_name)
                                   for video_name in video_names}
    return stimulus_set


def test_switch_inferences():
    stimulus_set = _build_stimulus_set()
    model = load_model("UniFormer-V2-L")
    switch_inferencer(model, CausalInferencer, fps='same', num_frames='same', 
                      duration=(0, 2000), layer_activation_format='same')
    model.start_recording('BRAIN', time_bins=[(100, 150), (150, 200), (200, 250)])
    model_assembly = model.look_at(stimulus_set)
    assert model_assembly is not None