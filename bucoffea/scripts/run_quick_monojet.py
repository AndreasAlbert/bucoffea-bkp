#!/usr/bin/env python

from bucoffea.helpers.dataset import extract_year
from bucoffea.processor.executor import run_uproot_job_nanoaod
from bucoffea.monojet import monojetProcessor
from bucoffea.helpers.cutflow import print_cutflow
from coffea.util import save
import coffea.processor as processor

def main():
    fileset = {
        # "Znunu_ht200to400" : [
        #     "./data/FFD69E5A-A941-2D41-A629-9D62D9E8BE9A.root"
        # ],
        # "NonthDM" : [
        #     "./data/24EE25F5-FB54-E911-AB96-40F2E9C6B000.root"
        # ]
        # "ttbardm_mmed10000_mchi1_nanoaodv5" : [
        #     "./data/ttbardm_mmed10000_mchi1_nanoaodv5/64888F08-B888-ED40-84A5-F321A4BEAC27.root",
        #     "./data/ttbardm_mmed10000_mchi1_nanoaodv5/DBCA1773-BF28-E54F-8046-5EB316C2F725.root"
        # ],
        # "a2HDM" : ["./data/a2HDM_monoz_mH900_ma200_2017_v5.root"]
        # "monozvec18" : ["./data/monozll_vec_mmed_1500_mxd_1_2017_v5.root"],
        # "wz_p8_2018" : ["./data/wz_p8_2018_v5.root"],
        # "wz_p8_2017" : ["./data/tt_amc_2017_v5.root"],
        # "wz_p8_2018" : ["./data/tt_amc_2018_v5.root"],
        # "monozvec17" : ["./data/monozll_vec_mmed_1500_mxd_1_2018_v5"]
        # "data_met_run2016c_v4" : [
        #     "./data/data_met_run2016c_v4.root"
        # ]
        # 'dy_zpt200_m50_mlm_2016_nanov4' : [
            # "./data/dy_zpt200_m50_mlm_2016_nanov4.root"
        # ],
        # "tt_amc_2017_v5" : ["./data/tt_amc_2017_v5.root"],
        # "tt_amc_2018_v5" : ["./data/tt_amc_2018_v5.root"],
        # "vector_monoj_mmed1500_mdm300_2017_v5" :[
        # "./data/vector_monoj_mmed1500_mdm300_2017_v5.root"
        # ]
        # "zjetsnunu_ht1200to2500_mg_2018_v5":[
        # "data/zjetsnunu_ht1200to2500_mg_2018_v5.root"
        # ]
        "SingleMuon_2018C" : [
            "./data/SingleMuon_2018C.root"
        ]
    }

    years = list(set(map(extract_year, fileset.keys())))
    assert(len(years)==1)

    for dataset, filelist in fileset.items():
        newlist = []
        for file in filelist:
            if file.startswith("/store/"):
                newlist.append("root://cms-xrd-global.cern.ch//" + file)
            else: newlist.append(file)
        fileset[dataset] = newlist

    for dataset, filelist in fileset.items():
        tmp = {dataset:filelist}
        output = run_uproot_job_nanoaod(tmp,
                                    treename='Events',
                                    processor_instance=monojetProcessor(years[0]),
                                    executor=processor.futures_executor,
                                    executor_args={'workers': 10, 'flatten': True},
                                    chunksize=500000,
                                    )
        save(output, f"monojet_{dataset}.coffea")
    # Debugging / testing output
    # debug_plot_output(output)
        print_cutflow(output, outfile=f'monojet_cutflow_{dataset}.txt')

if __name__ == "__main__":
    main()