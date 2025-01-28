# import sys
# specified_dir = r'S:\SystemDefault\Desktop\project\KGRAG\kag'
# if specified_dir not in sys.path:
#     sys.path.append(specified_dir)

import os
import logging

import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from kag.common.env import init_kag_config
from kag.common.benchmarks.evaluate import Evaluate
from kag.solver.logic.solver_pipeline import SolverPipeline

from knext.reasoner.client import ReasonerClient

from kag.solver.logic.core_modules.lf_solver import LFSolver
from kag.solver.implementation.default_kg_retrieval import KGRetrieverByLlm
from kag.solver.implementation.default_reasoner import DefaultReasoner
from kag.solver.implementation.lf_chunk_retriever import LFChunkRetriever
from kag.interface.solver.lf_planner_abc import LFPlannerABC

logger = logging.getLogger(__name__)

class QaDemo:

    """
    init for kag client
    """

    def __init__(self, configFilePath):
        self.configFilePath = configFilePath
        init_kag_config(self.configFilePath)

    def qa(self, query):
        resp = SolverPipeline()
        answer, trace_log = resp.run(query)
        logger.info(f"\n\nThe answer for '{query}' is: {answer}\n\n")
        return answer, trace_log

    def qaWithoutLogicForm(self, query):
        lf_solver = LFSolver(chunk_retriever=LFChunkRetriever(),
                             kg_retriever=KGRetrieverByLlm())
        reasoner = DefaultReasoner(lf_planner=LFPlannerABC(), lf_solver=lf_solver)
        resp = SolverPipeline(reasoner=reasoner)
        answer, trace_log = resp.run(query)
        logger.info(f"\n\nso the answer for '{query}' is: {answer}\n\n")
        return answer, trace_log
    
    def fakeqa(self, query):
        answer, trace_log = ["虚损病","肝郁脾虚","疏肝理脾，疏肝健脾","逍遥散"], "log"
        return answer, trace_log
    
    def parallelQaAndEvaluate(
            self, qaFilePath, resFilePath, threadNum=1, upperLimit=10
    ):
        def process_sample(data):
            try:
                sample_idx, sample = data
                sample_id = sample["id"]
                question = sample["clinical_info"]
                gold = [sample["disease"], sample["syndrome"], sample["cura_method"], sample["prescription"]]
                
                print("The answer is: ",gold)
                ################################################################################
                prediction, traceLog = self.qa(question)
                ################################################################################
                print("prediction is: ", prediction)

                evaObj = Evaluate()

                # predictionlist: List[str], goldlist: List[str]
                metrics = evaObj.getBenchMark(prediction, gold)
                return sample_idx, sample_id, prediction, metrics, traceLog
            except Exception as e:
                import traceback

                logger.warning(
                    f"process sample failed with error:{traceback.print_exc()}\nfor: {data}"
                )
                return None

        qaList = json.load(open(qaFilePath, "r", encoding="utf-8"))
        total_metrics = {
            "em": 0.0,
            "f1": 0.0,
            "answer_similarity": 0.0,
            "processNum": 0,
        }
        with ThreadPoolExecutor(max_workers=threadNum) as executor:
            futures = [
                executor.submit(process_sample, (sample_idx, sample))
                for sample_idx, sample in enumerate(qaList[:upperLimit])
            ]
            for future in tqdm(
                    as_completed(futures),
                    total=len(futures),
                    desc="parallelQaAndEvaluate completing: ",
            ):
                result = future.result()
                if result is not None:
                    sample_idx, sample_id, prediction, metrics, traceLog = result
                    sample = qaList[sample_idx]

                    sample["prediction"] = prediction
                    sample["traceLog"] = traceLog
                    sample["em"] = str(metrics["em"])
                    sample["f1"] = str(metrics["f1"])

                    total_metrics["em"] += metrics["em"]
                    total_metrics["f1"] += metrics["f1"]
                    total_metrics["answer_similarity"] += metrics["answer_similarity"]
                    total_metrics["processNum"] += 1

                    if sample_idx % 50 == 0:
                        with open(resFilePath, "w", encoding="utf-8") as f:
                            json.dump(qaList, f, ensure_ascii=False)

        with open(resFilePath, "w", encoding="utf-8") as f:
            json.dump(qaList, f, ensure_ascii=False)

        res_metrics = {}
        for item_key, item_value in total_metrics.items():
            if item_key != "processNum":
                res_metrics[item_key] = item_value / total_metrics["processNum"]
            else:
                res_metrics[item_key] = total_metrics["processNum"]
        return res_metrics


if __name__ == "__main__":

    configFilePath = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "../kag_config.cfg"
    )

    # os.environ["KAG_PROJECT_ID"] = "tcm"
    # os.environ["KAG_PROJECT_HOST_ADDR"] = "localhost:10000"

    # project_id = os.getenv("KAG_PROJECT_ID")
    # host_addr = os.getenv("KAG_PROJECT_HOST_ADDR")
    # sc = ReasonerClient(host_addr, project_id, )
    # param = {
    #     "spg.reasoner.plan.pretty.print.logger.enable": "true"
    # }

    # single query
    # singleQa = QaDemo()
    # query = "小儿呕吐有哪些典型证候？"
    # answer,trace_log = singleQa.qa(query)
    # print(f"Question: {query}")
    # print(f"Answer: {answer}")
    # print(f"TraceLog: {trace_log}")

    # batch query
    qaListFile = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "../CMedSD.json"
    )
    reListFile = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "../CMedSD_res.json"
    )
    batchQa = QaDemo(configFilePath=configFilePath)
    res_metrics = batchQa.parallelQaAndEvaluate(qaListFile, reListFile, threadNum=1, upperLimit=10)
    print(res_metrics)
    
    # go to check every query f1 score -> ./data/CMedSD_res.json.json
