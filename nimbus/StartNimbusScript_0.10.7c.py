#!/usr/bin/env python
# encoding: utf-8
"""
    StartNimbusScriptpy
    Created by Jason Warner on 2012-04-30.
    Copyright (c) 2012 __MyCompanyName__. All rights reserved.
    """

import sys
import os
import glob
import csv
import time
import string

path_to_seqware = "/home/sbsuser/seqware-pipeline-0.12.1-r4898.jar"
root_folder = ""
machine_to_easymachine_dict=dict()
machine_to_easymachine_dict["M00165"] = "MISEQ1"
machine_to_easymachine_dict["M00604"] = "MISEQ2"
machine_to_easymachine_dict["M00695"] = "MISEQ3"
machine_to_easymachine_dict["M00936"] = "MISEQ4"
machine_to_easymachine_dict["M00935"] = "MISEQ5"
machine_to_easymachine_dict["M00937"] = "MISEQ6"
machine_to_easymachine_dict["SN7001141"] = "HISEQ1"



# determines study name based on the directory of the sequencing run
def get_all_seq_runs():
    seq_run_dir_list = []
    path_dict = dict()
    for dirname in os.listdir('/mnt/data/Runs'):
        if os.path.isdir(os.path.join('/mnt/data/Runs/',dirname)):
            try:
                temp = os.path.join('/mnt/data/Runs/',dirname)
                open (os.path.join(temp,'CompletedJobInfo.xml'))
                print dirname
                try:
                    open (os.path.join(temp,'OnNimbus.txt'))
                except:
                    seq_run_dir_list.append(temp)
            except:
                pass
    seq_run_dir_list.sort()
    for item in seq_run_dir_list:
        print item
    return seq_run_dir_list

#Rename filenames to include the run name
def RenameFiles(filepath):
    dirname = get_study_name(filepath.split("/")[-1])
    print dirname + " is the dirname"
    os.system("mv " + filepath + "/UNALIGNED/Project_DefaultProject/*/* "+ filepath + "/UNALIGNED/Project_DefaultProject/" )
    os.chdir(filepath + "/UNALIGNED/Project_DefaultProject")
    os.system("rename GPP " + dirname + "_GPP *" )
    os.system("rename Control " + dirname + "_Control *" )
    os.system("rename RD " + dirname + "_RD *" )
    return

# Demultiplex Fastq files
def DemultiplexFastq(seq_run_path, study_type):
    if study_type == "haloplex":
        os.system("perl /illumina/pipeline/CASAVA_1.8.2/bin/configureBclToFastq.pl --input-dir " + seq_run_path + "/Data/Intensities/BaseCalls/ --output-dir " +seq_run_path+"/UNALIGNED --sample-sheet " + seq_run_path + "/TestSampleSheet2.csv --use-bases-mask=Y*,I*,Y*,N* --ignore-missing-bcl --ignore-missing-stats --mismatches 0 --force")
    else:
        os.system("perl /illumina/pipeline/CASAVA_1.8.2/bin/configureBclToFastq.pl --input-dir " + seq_run_path + "/Data/Intensities/BaseCalls/ --output-dir " +seq_run_path+"/UNALIGNED --sample-sheet " + seq_run_path + "/TestSampleSheet2.csv --use-bases-mask=Y*,I*,I*,Y* --ignore-missing-bcl --ignore-missing-stats --mismatches 0 --force")

    print("cd " + seq_run_path + "/UNALIGNED")
    os.chdir(seq_run_path +"/UNALIGNED" )
    os.system("pwd")
    os.system("nohup make -j 8")

#Create the study on Nimbus
def get_study_name(orig_string):
    studyname =""
    words = orig_string.split("_")
    study_name="20"+words[0]+"_"+machine_to_easymachine_dict[words[1]]
    return study_name

#Read the sample sheet
def read_sample_sheet(root_folder):
    print "Now reading sample sheet"
    fin  = open(root_folder+"/SampleSheet.csv", "rU")
    print root_folder + " is the root"
    # each run will have 4 samples and 4 controls
    # for each sample I need a pair of barcodes
    #col headings: 0:Sample_ID 1:Sample_Name 2:Sample_Plate 3:Sample_Well 4:Sample_Project 5:index 6:I7_Index_ID 7:index2 8:I5_Index_ID 9:Description	GenomeFolder
    read_data=0 #variable used to avoid header info
    sample_list =[] # list that contains sample: ex.: GPP00001_P1
    samplename_list =[]
    study_type=""
    temp ="" # string to contain sample name
    barcode_from_sampleID_dict=dict() 
    reader = csv.reader(fin)
    for row in reader:
        dual_barcode =""
        if read_data:
            if row[0] == "Sample_ID":
                pass
            else:
                if row[7]=="":
                    dual_barcode=row[5]
                else:
                    dual_barcode = row[5]+"-"+row[7]
                barcode_from_sampleID_dict[row[0]]=dual_barcode
                words = root_folder.split("_")
                sample_list.append(row[0])
                machine_to_easymachine_dict[words[1]]
                prefix="20"+words[0]+"_"+machine_to_easymachine_dict[words[1]]+"_"+row[0]+"_"+dual_barcode
                study_name="20"+words[0]+"_"+machine_to_easymachine_dict[words[1]]
                samplename_list.append(prefix)
        if row[0] == "[Data]":
            read_data=1
        elif row[0] == "Project Name":
            study_type = row[1]
    if study_type.strip == "":
        study_type="mtseek"
    return study_name, samplename_list, sample_list, barcode_from_sampleID_dict, study_type

# Transform MISEQ sample sheet into a CASAVA-style sample sheet
def create_casava_sample_sheet(root_folder,sample_list, barcode_from_sampleID_dict):
    spamWriter = csv.writer(open("/mnt/data/Runs/"+root_folder+"/TestSampleSheet2.csv", 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamWriter.writerow(['FCID','Lane', 'SampleID','SampleRef','Index','Description','Control','Recipe','Operator','SampleProject'])
    for sample in sample_list:
        spamWriter.writerow(['000000000-A0U0R','1',sample,'',barcode_from_sampleID_dict[sample],'N','','','','DefaultProject'])

# Create a new study on Nimbus
def CreateStudyNameOnNimbus(title,study_type):
    print "Creating study"
    os.system("java -jar " + path_to_seqware + " -p net.sourceforge.seqware.pipeline.plugins.Metadata -- --table study --create --field 'title::" + title + "' --field 'description::description' --field 'accession::NA' --field 'center_name::Courtagen' --field 'center_project_name::Courtagen " +study_type + "' --field study_type::4 > /home/sbsuser/NewStudy.txt")
    return

# Create a new experiment on Nimbus
def CreateExperimentNameOnNimbus(title, accession):
    print "Creating Experiment"
    os.system("java -jar " + path_to_seqware + " -p net.sourceforge.seqware.pipeline.plugins.Metadata -- --table experiment --create --field 'title::" + title + "_exp' --field 'description::description' --field study_accession::"+str(accession)+" --field platform_id::26 > /home/sbsuser/NewStudy.txt")
    return

# Create new sample on Nimbus
def CreateSampleOnNimbus(title, accession):
    os.system("java -jar " + path_to_seqware + " -p net.sourceforge.seqware.pipeline.plugins.Metadata -- --table sample --create --field 'title::" + title + "' --field 'description::description' --field experiment_accession::"+str(accession)+" --field organism_id::31 > /home/sbsuser/NewStudy.txt")
    return

#create the mito ini for workflows on Nimbus
def CreateMitoIni(sample_name):
    sample_name=sample_name.split("/")[-1]
    spamWriter = csv.writer(open("/home/sbsuser/mito.ini", 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamWriter.writerow(['rg_sample_name='+sample_name])
    spamWriter.writerow(['run_ends=2'])
    filename2="input_fastq_2=s3://newco.uploads/"+ sample_name + "/20" + sample_name + "_L001_R2_001.fastq.gz"
    filename1="input_fastq_1=s3://newco.uploads/"+ sample_name + "/20" + sample_name + "_L001_R1_001.fastq.gz"
    spamWriter.writerow([filename2])
    spamWriter.writerow([filename1])
    spamWriter.writerow(['rg_sample_name='+sample_name])
    spamWriter.writerow(['fastq_quality_filter=true'])
    spamWriter.writerow(['novoalign_t_param=default'])
    spamWriter.writerow(['fastq_adapter_clip=true'])
    spamWriter.writerow(['adapter_min_result_len=20'])
    spamWriter.writerow(['quality_trim_min_len=20'])
    spamWriter.writerow(['varscan_indel_strand_filter=1'])
    spamWriter.writerow(['hmito_min_freq=0.2'])
    spamWriter.writerow(['varscan_indel_min_freq_for_hom=0.75'])
    spamWriter.writerow(['varscan_snp_min_avg_qual=20'])
    spamWriter.writerow(['varscan_snp_min_var_freq=0.01'])
    spamWriter.writerow(['min_percent_bases=90'])
    spamWriter.writerow(['varscan_indel_min_coverage=500'])
    spamWriter.writerow(['novoalign_gap_extend_param=15'])
    spamWriter.writerow(['varscan_snp_strand_filter=1'])
    spamWriter.writerow(['min_qual_score=20'])
    spamWriter.writerow(['fastq_quality_trim=true'])
    spamWriter.writerow(['adapter_min_match_len=10'])
    spamWriter.writerow(['adapter_str=GATCGGAAGAGCTCGTATGCCGTCTTCTGCTTG,ACACTCTTTCCCTACACGACGCTCTTCCGATCT,GATCGGAAGAGCGGTTCAGCAGGAATGCCGAG,ACACTCTTTCCCTACACGACGCTCTTCCGATCT'])
    spamWriter.writerow(['varscan_indel_min_var_freq=0.01'])
    spamWriter.writerow(['varscan_indel_min_reads2=20'])
    spamWriter.writerow(['workflow_temp=/mnt/gluster/rep-ue'])
    spamWriter.writerow(['output_prefix=s3://nimbusinformatics.analysis/'])
    spamWriter.writerow(['varscan_snp_p_value=0.000000000000000000000000000001'])
    spamWriter.writerow(['varscan_snp_min_freq_for_hom=0.75'])
    spamWriter.writerow(['quality_trim_min_qual=5'])
    spamWriter.writerow(['varscan_snp_min_coverage=500'])
    spamWriter.writerow(['novoalign_gap_open_param=40'])
    spamWriter.writerow(['varscan_snp_min_reads2=20'])
    spamWriter.writerow(['output_dir=results'])
    spamWriter.writerow(['varscan_indel_p_value=0.000000000000000000000000000001'])
    spamWriter.writerow(['varscan_indel_min_avg_qual=20'])
    return

def CreateNucIni(sample_name,filelist_R1,filelist_R2):
    tempnames = sample_name.split("/")[-1].split("-")[0].split("_")
    sample_name=str(tempnames[0]+"_"+tempnames[1]+"_"+tempnames[2])
    spamWriter = csv.writer(open("/home/sbsuser/nucseek.ini", 'wb'), delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamWriter.writerow(['run_ends=2'])
    spamWriter.writerow(['rg_sample_name='+sample_name])
    filename2='input_fastq_2='+str(filelist_R2)
    filename1='input_fastq_1='+str(filelist_R1)
    spamWriter.writerow([filename2])
    spamWriter.writerow([filename1])
    spamWriter.writerow(['output_dir=results'])
    spamWriter.writerow(['output_prefix=s3://newco.uploads/'])
    spamWriter.writerow(['adapter_str=GATCGGAAGAGCTCGTATGCCGTCTTCTGCTTG,ACACTCTTTCCCTACACGACGCTCTTCCGATCT,GATCGGAAGAGCGGTTCAGCAGGAATGCCGAG,ACACTCTTTCCCTACACGACGCTCTTCCGATCT,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATTAAAAAAAA,TTTTTTTTAATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACAGCACGCTCTTCCGATCT,AGATCGGAAGAGCACACGTCTGAACTCCAGTCACCCTTCGATCTCGTATGCCGTCTTCTGCTTGAAAAAAAAAAA,TTTTTTTTTTTCAAGCAGAAGACGGCATACGAGATCGAAGGGTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT'])
    spamWriter.writerow(['unmark_duplicates=false'])
    spamWriter.writerow(['fastq_quality_filter=true'])
    spamWriter.writerow(['fastq_adapter_clip=true'])
    spamWriter.writerow(['adapter_min_result_len=20'])
    spamWriter.writerow(['workflow_temp=/mnt/gluster/rep-ue'])
    spamWriter.writerow(['quality_trim_min_len=20'])
    spamWriter.writerow(['quality_trim_min_qual=5'])
    spamWriter.writerow(['min_percent_bases=90'])
    spamWriter.writerow(['mark_duplicates=false'])
    spamWriter.writerow(['fastq_quality_trim=true'])
    spamWriter.writerow(['min_qual_score=20'])
    spamWriter.writerow(['adapter_min_match_len=10'])
    return

# launch the mtSEEK workflow on Nimbus
def LaunchMtseekWorkflow(accession):
    os.system("java -jar " + path_to_seqware + " -p net.sourceforge.seqware.pipeline.plugins.WorkflowLauncher -- --ini-files mito.ini --workflow-accession 66779 --schedule --parent-accessions " + str(accession))
    return

def LaunchNucseekWorkflow(accession):
    os.system("java -jar " + path_to_seqware + " -p net.sourceforge.seqware.pipeline.plugins.WorkflowLauncher -- --ini-files nucseek.ini --workflow-accession 66764 --schedule --parent-accessions " + str(accession))
    return


def TrimFastq( filepath, sample_name ):
    path_to_shredder = "/home/sbsuser/lyons/shredder.jar"
    path_to_read1 = filepath + "/UNALIGNED/Project_DefaultProject/20"+ sample_name + "_L001_R1_001.fastq.gz"
    path_to_read1_trimmed = filepath + "/UNALIGNED/Project_DefaultProject/20"+ sample_name + "_L001_R1_001.trimmed.fastq.gz"
    path_to_read2 = filepath + "/UNALIGNED/Project_DefaultProject/20"+ sample_name + "_L001_R2_001.fastq.gz"		# Submit the job for each sample
    path_to_read2_trimmed = filepath + "/UNALIGNED/Project_DefaultProject/20"+ sample_name + "_L001_R2_001.trimmed.fastq.gz"		# Submit the job for each sample
    #trim with scala using picard to read/write
    shredder_cmd = "java -jar %s %s /dev/stdout | gzip -c > %s" % (path_to_shredder, path_to_read1, path_to_read1_trimmed )
    os.system( shredder_cmd )
    shredder_cmd = "java -jar %s %s /dev/stdout | gzip -c > %s" % (path_to_shredder, path_to_read2, path_to_read2_trimmed )
    os.system(shredder_cmd)
    return path_to_read1_trimmed ,path_to_read2_trimmed 


# upload paired end data and associate with accession
def UploadSampleToNimbus(accession, filepath, sample_name):
    path_to_S3_folder = "s3://newco.uploads/"+sample_name+"/"
    path_to_S3_output_folder ="s3://newco.uploads/"+sample_name+"/"
    print "The accession is " +str(accession)
    path_to_read1 = filepath + "/UNALIGNED/Project_DefaultProject/20"+ sample_name + "_L001_R1_001.fastq.gz"
    path_to_read2 = filepath + "/UNALIGNED/Project_DefaultProject/20"+ sample_name + "_L001_R2_001.fastq.gz"		# Submit the job for each sample

    uploadOK = 0
    while uploadOK == 0:
        os.system("java -jar " + path_to_seqware + " -p net.sourceforge.seqware.pipeline.plugins.ModuleRunner -- --module net.sourceforge.seqware.pipeline.modules.utilities.ProvisionFiles --metadata-output-file-prefix " + path_to_S3_folder +" --metadata-parent-accession " +str(accession)+ " --metadata-processing-accession-file new_accession.txt -- -im jar::chemical/seq-na-fastq-gzip::"+path_to_read1+ " -im jar::chemical/seq-na-fastq-gzip::"+path_to_read2 + " -o " + path_to_S3_output_folder)
        time.sleep(20)
        os.system("s3cmd ls " + path_to_S3_folder + "20" + sample_name + "_L001_R1_001.fastq.gz > read1ls.txt")
        os.system("s3cmd ls " + path_to_S3_folder + "20" + sample_name + "_L001_R2_001.fastq.gz > read2ls.txt")
        print str(os.path.getsize("read1ls.txt"))
        print str(os.path.getsize("read2ls.txt"))
        if os.path.getsize("read1ls.txt") == 0 or os.path.getsize("read2ls.txt") == 0:
            uploadOK = 0
        else:
            time.sleep(20)
            uploadOK = 1
        
    
    return

def UploadNucSeekSampleToNimbus(accession, filepath, sample_name, filelist_R1,filelist_R2):
    sample_folder = sample_name.split("_")[0]+"_" + sample_name.split("_")[1]+"_NUCSEEK"
    path_to_S3_folder = "s3://newco.uploads/"+sample_folder+"/"
    path_to_S3_output_folder ="s3://newco.uploads/"+sample_folder+"/"
    print "The accession is " +str(accession)
    path_to_read1 = filepath + "/UNALIGNED/Project_DefaultProject/20"+ sample_name + "_L001_R1_001.fastq.gz"
    path_to_read2 = filepath + "/UNALIGNED/Project_DefaultProject/20"+ sample_name + "_L001_R2_001.fastq.gz"		# Submit the job for each sample
    
    uploadOK = 0
    while uploadOK == 0:
        os.system("java -jar " + path_to_seqware + " -p net.sourceforge.seqware.pipeline.plugins.ModuleRunner -- --module net.sourceforge.seqware.pipeline.modules.utilities.ProvisionFiles --metadata-output-file-prefix " + path_to_S3_folder +" --metadata-parent-accession " +str(accession)+ " --metadata-processing-accession-file new_accession.txt -- -im jar::chemical/seq-na-fastq-gzip::"+path_to_read1+ " -im jar::chemical/seq-na-fastq-gzip::"+path_to_read2 + " -o " + path_to_S3_output_folder)
        time.sleep(20)
        os.system("s3cmd ls " + path_to_S3_folder + "20" + sample_name + "_L001_R1_001.fastq.gz > read1ls.txt")
        os.system("s3cmd ls " + path_to_S3_folder + "20" + sample_name + "_L001_R2_001.fastq.gz > read2ls.txt")
        print str(os.path.getsize("read1ls.txt"))
        print str(os.path.getsize("read2ls.txt"))
        if os.path.getsize("read1ls.txt") == 0 or os.path.getsize("read2ls.txt") == 0:
            uploadOK = 0
        else:
            time.sleep(20)
            uploadOK = 1
    
    if filelist_R2 == "":
        filelist_R2 = path_to_S3_folder + "20" + sample_name + "_L001_R2_001.fastq.gz"
        filelist_R1 = path_to_S3_folder + "20" + sample_name + "_L001_R1_001.fastq.gz"
    else:
        filelist_R2 = filelist_R2 + "," + path_to_S3_folder + "20" + sample_name + "_L001_R2_001.fastq.gz"
        filelist_R1 = filelist_R1 + "," + path_to_S3_folder + "20" + sample_name + "_L001_R1_001.fastq.gz"
    return filelist_R1,filelist_R2

# Just grab and reutrn the ID associated with study/experiment/sample
def GetSWID():
    os.chdir("/home/sbsuser")
    os.system("grep SWID: NewStudy.txt > grep.txt")
    fin  = open("/home/sbsuser/grep.txt", "rU")
    reader = csv.reader(fin)
    for row in reader:
        SWID = row[0].split(" ")[1]
        print SWID
        return SWID

def MarkRunAsCompleted(root_folder):
    spamWriter = csv.writer(open("/mnt/data/Runs/"+root_folder+"/OnNimbus.txt", 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamWriter.writerow(['This run does not need to be analyzed.'])
    return

# All the work in done here
def main():
    while 1==1:
	# Create/get sample IDs through sample sheet
        all_seq_runs_list = get_all_seq_runs()
        for run in all_seq_runs_list:
            filelist_R1=""
            filelist_R2=""
            study_name, samplename_list, sample_list, barcode_from_sampleID_dict, study_type = read_sample_sheet(run)
            create_casava_sample_sheet(run.split("/")[-1],sample_list, barcode_from_sampleID_dict)
            
            DemultiplexFastq(run, study_type)
            RenameFiles(run)
            if study_type.lower().strip() == "haloplex" or study_type.lower().strip() == "halo-plex":
                version = "0.10.6"
                study_type = "nucSEEK"
            else:
                version = "0.10.9"
                study_type = "mtSEEK"
            
                    # CREATE STUDY
            CreateStudyNameOnNimbus("20"+study_name.split("/")[-1]+"_"+study_type+"_"+version,study_type)
            time.sleep(5)
            SWID=GetSWID()
        
            # CREATE EXPERIMENT
            CreateExperimentNameOnNimbus("20"+study_name.split("/")[-1]+"_"+study_type+"_"+version,SWID)
            time.sleep(5)
            SWID=GetSWID()
            print "study type is:" + study_type
            
            if study_type == "nucSEEK":
                print "Trying to create sample"
                tempnames = samplename_list[0].split("/")[-1].split("-")[0].split("_")
                CreateSampleOnNimbus(tempnames[0]+"_"+tempnames[1]+"_"+tempnames[2],SWID)
                time.sleep(5)
                SampleSWID2=GetSWID()
            # CREATE SAMPLES
            for item in samplename_list:
                if study_type.lower().strip() == "mtseek" or study_type.lower().strip() =="mt-seek":
                    CreateSampleOnNimbus(item.split("/")[-1],SWID)
                    time.sleep(5)
                    SampleSWID2=GetSWID()
                    print str(SampleSWID2) + " is the sample ID"
                    UploadSampleToNimbus(SampleSWID2, run, item.split("/")[-1])
                    time.sleep(10)
                    CreateMitoIni(item)
                    LaunchMtseekWorkflow(SampleSWID2)
                elif study_type.lower().strip() == "nucseek":
                    print str(SampleSWID2) + " is the sample ID"
                    print filelist_R1
                    filelist_R1,filelist_R2 = UploadNucSeekSampleToNimbus(SampleSWID2, run, item.split("/")[-1],filelist_R1,filelist_R2)
                    time.sleep(10)
            if study_type == "nucSEEK":
                CreateNucIni(item,filelist_R1,filelist_R2)
                LaunchNucseekWorkflow(SampleSWID2)
                
            MarkRunAsCompleted(run.split("/")[-1])
        print "Analysis daemon is running. Do not close window. Sleeping for 5 minutes."
        time.sleep(300)
   
if __name__ == '__main__':
	main()
