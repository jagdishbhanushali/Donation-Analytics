from heapq import heappush
import datetime
import os
import math
import sys

input_file=sys.argv[1] #"../input/itcont.txt"
output_path="../output/repeat_donors.txt"
percentile_file_path=sys.argv[2]
with open(percentile_file_path,"r") as f:
    percentile=float(f.read())

class heap_percentile:
    def __init__(self):
        self.sorted_list = []

    def add(self, value):
        push(self.sorted_list, value)

recipients ={}
donors={}

def get_percentile(element_list,percentile):
    index = math.ceil((percentile/100)*len(element_list))
    return element_list[index-1]

def write_file(line):
    with open(output_path,"a") as f:
        f.write(line+"\n")

def get_repeat_donor_recipient(cmte_id,zip_code,year):
    recipient_id=cmte_id+"_"+zip_code
    if recipient_id in recipients:
        if year in recipients[recipient_id]:
            recipient_obj=recipients[recipient_id][year]
            recipient_obj["repeated_donor_count"]=recipient_obj["repeated_donor_count"]+1
            # print(recipient_obj)
            repeated_percentile_value=get_percentile(recipient_obj["amount_list"],percentile)
            line=cmte_id+"|"+ zip_code+"|"+year+"|"+str(repeated_percentile_value)+"|"+str(recipient_obj["total_amount"])+"|"+str(recipient_obj["repeated_donor_count"])
            write_file(line)
            # print(line)


def add_donor(donor_name,amount,cmte_id,tr_date,zip_code):
    donor_id=donor_name+"_"+zip_code
    year=tr_date[-4:]
    donor_obj={}
    donor_obj["name"]=donor_name
    donor_obj["amount"]=amount
    donor_obj["cmte_id"]=cmte_id
    donor_obj["zip_code"]=zip_code
    donor_obj["tr_date"]=tr_date

    if(donor_id in donors):
        donors[donor_id][year] = donor_obj
        get_repeat_donor_recipient(cmte_id,zip_code,year)
    else:
        donors[donor_id]={}
        donors[donor_id][year]=donor_obj

def add_recipient(donor_name,amount,cmte_id,tr_date,zip_code):
    recipient_id=cmte_id+"_"+zip_code
    year = tr_date[-4:]
    recipient_obj={}
    if recipient_id in recipients:
        if year in recipients[recipient_id]:
            recipient_obj=recipients[recipient_id][year]
            amount_list=recipient_obj["amount_list"]
            heappush(amount_list,amount)
            recipient_obj["amount_list"]=amount_list
            recipient_obj["total_amount"] = recipient_obj["total_amount"]+amount
            recipient_obj["total_count"] = recipient_obj["total_count"] + 1
        else:
            amount_list = []
            heappush(amount_list, amount)
            recipient_obj["amount_list"] = amount_list
            recipient_obj["total_amount"] = amount
            recipient_obj["tr_date"] = tr_date
            recipient_obj["total_count"] = 1
            recipient_obj["repeated_donor_count"] = 0
            recipients[recipient_id][year] = recipient_obj
    else:
        amount_list=[]
        heappush(amount_list,amount)
        recipient_obj["amount_list"]=amount_list
        recipient_obj["total_amount"] =  amount
        recipient_obj["tr_date"] = tr_date
        recipient_obj["total_count"] = 1
        recipient_obj["repeated_donor_count"] = 0
        recipients[recipient_id]={"cmte_id":cmte_id,"zip_code":zip_code}
        recipients[recipient_id][year] = recipient_obj


def process(line,consider_other_id=False):
    # all_fields="C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|384||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337".strip().split('|')
    all_fields=line.strip().split('|')
    field_index=[0,7,10,13,14,15] #CMTE_ID,Name,ZIP_CODE,TRANSACTION_DT,TRANSACTION_AMT,OTHER_ID
    fields=[all_fields[i] for i in field_index]
    #Checking CMTEID, TRANSACTION_AMT for non-empty and OTHER_ID for empty
    if(fields[5]=="" and fields[0]!=""):
        tr_date=get_date(fields[3])
        zip_code=get_zip(fields[2])
        if(tr_date and zip_code):
            # print(fields)
            cmte_id = fields[0]
            donor_name=fields[1]
            amount=int(fields[4])
            add_recipient(donor_name, amount, cmte_id, tr_date, zip_code)
            add_donor(donor_name,amount,cmte_id,tr_date,zip_code)




def get_zip(data):
    zip_code = data[:5]
    # Ignoring ZIP length less than 5
    if len(zip_code) < 5:
        return False
    return zip_code

def get_date(data):
    try:
        #Checking proper date format. ALso works for empty date string
        if(datetime.datetime.strptime(data,"%m%d%Y")):
            tr_date = data
    except:
        print("Date Exception")
        return False
    return tr_date

if __name__ == '__main__':

    if (os.path.exists(output_path)):
        os.remove(output_path)

    with open (input_file) as f:
        for line in f:
            process(line)
            # break
