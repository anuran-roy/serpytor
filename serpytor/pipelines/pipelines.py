from typing import List, Tuple, Optional, Dict, Callable, Iterable, Any, Union
from serpytor.pipelines.exceptions import (
    CriticalPipelineError,
    PipelineError,
    PipelineWarning,
    PipelineInfo,
    PipelineDebugInfo,
)
import traceback
from serpytor.analytics.decorators import get_execution_time


class Pipeline:
    """Create pipelines by stacking functions on top of each other.

    Some conventions to follow:

    1. The first function must be a producer function that outputs data.
    2. The rest of the functions must be consumer functions that take in data AND return data.


    This is done to ensure that the pipeline is not broken, and that there is a single source of initial data.
    """

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
    def execute(self, method: Callable, data: Any, *args, **kwargs) -> None:
        """Executor for pipelined functions"""
        try:
            return method(data, *args, **kwargs)
        except Exception as e:
            raise PipelineError("Error in executing pipeline.") from e

    @get_execution_time
    def execute_pipeline(self, *args, **kwargs) -> None:
        try:
            try:
                data = None
                for (
                    pipelined_callable,
                    pipelined_args,
                    pipelined_kwargs,
                ) in self.pipeline:
                    if len(pipelined_args) == 0:
                        pipelined_args = self.global_args
                    pipelined_kwargs = self.global_kwargs | kwargs
                    data = self.execute(
                        pipelined_callable, data, *pipelined_args, **pipelined_kwargs
                    )

                print("Pipeline execution complete.")
                return data

            except Exception as e:
                traceback.print_exc()
                raise PipelineError(
                    "Could not execute one or more parts of the pipeline."
                )
        except PipelineError as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            raise CriticalPipelineError(f"Error in pipeline flow!")


if __name__ == "__main__":
    """Set up a demo pipeline"""

    def producer(*args, **kwargs):
        return [1, 0, 1, 0, 1]

    def proc1(data, *args, **kwargs):
        print(data)
        mod_data = [i + 1 for i in data]
        return mod_data

    def proc2(data, *args, **kwargs):
        print(data)
        mod_data2 = [i**2 for i in data]
        return mod_data2

    pipe = Pipeline(pipeline=[(producer, [], {}), (proc1, [], {}), (proc2, [], {})])

    finished_data = pipe.execute_pipeline()
    print(finished_data)
