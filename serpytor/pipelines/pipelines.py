from typing import List, Tuple, Optional, Dict, Callable, Iterable, Any, Union
from .exceptions import (
    CriticalPipelineError,
    PipelineError,
    PipelineWarning,
    PipelineInfo,
    PipelineDebugInfo,
)
import traceback
from serpytor.analytics.decorators import get_execution_time


class Pipeline:
    def __init__(self, pipeline: List[Callable], *args, **kwargs) -> None:
        """
        Create pipelines that can be augmented, modified or changed using monkey-patching.
        """

        self.pipeline: List[Callable] = pipeline
        self.pipeline_length: int = 0
        self.global_args = args
        self.global_kwargs = kwargs

    def add_to_pipeline(self, callable: Callable, index: int = 0) -> None:
        self.pipeline.insert(index, callable)
        self.pipeline_length += 1

    def remove_from_pipeline(self, index: int = 0) -> None:
        if index >= self.pipeline_length:
            raise CriticalPipelineError(
                f"Cannot remove from pipeline. Length of pipeline = {self.pipeline_length}, element referred = {index+1}"
            )
        else:
            self.pipeline.remove(self.pipeline[index])

    @get_execution_time
    def execute(self, callable: Callable, *args, **kwargs) -> None:
        try:
            return callable(*args, **kwargs)
        except Exception as e:
            raise PipelineError("Error in executing pipeline.") 

    @get_execution_time
    def execute_pipeline(self, *args, **kwargs) -> None:
        try:
            try:
                for pipelined_callable, pipelined_args, pipelined_kwargs in self.pipeline:
                    if len(pipelined_args) == 0:
                        pipelined_args = self.global_args
                    pipelined_kwargs = self.global_kwargs | kwargs
                    self.execute(pipelined_callable, *pipelined_args, **pipelined_kwargs)

                print("Pipeline execution complete.")
            except Exception as e:
                traceback.print_exc()
                raise PipelineError("Could not execute one or more parts of the pipeline.")
        except PipelineError as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            raise CriticalPipelineError(f"Error in pipeline flow!")
