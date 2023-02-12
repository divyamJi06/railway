import io
import xlsxwriter
import ast


def WriteToExcel(data,type):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    if "ledger" in type:
        getLedger(data,workbook)
    elif "trains" in type:
        getTrain(data,workbook)
    else:
        getBill(data,workbook)

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data

def formatDate(date):
    date  = date.strip()
    if(len(date)<=1):
        return "0{}".format(date)
    return date
def updateDate(data):
    data = data.replace("datetime.datetime","")
    data = data.replace("(",'"')
    data = data.replace(")",'"')
    ledger_data=ast.literal_eval(data)
    for index in range(len(ledger_data)):
        data = ledger_data[index]
        date = data['date']
        newDate = date.split(",")
        newDateToBeReturned  = "{}/{}/{}".format(formatDate(newDate[2]),formatDate(newDate[1]),newDate[0],)
        ledger_data[index]['date'] = newDateToBeReturned
    return ledger_data
def setUserInfo(data, workbook, worksheet):
    headings = data['heading']
    user = data['user']
    border_left = workbook.add_format({})
    border_left.set_left(1)
    align = {}
    for i in range(1, 27):
        align[i] = chr(i+64)
    no_of_fields = len(headings)

    worksheet.merge_range('A2:{}4'.format(align[no_of_fields]), user["name"], workbook.add_format({
        'bold': True,
        'font_size': 24,
        'align': 'center',
        'valign': 'vcenter'
    }))
    worksheet.merge_range('A5:{}5'.format(align[no_of_fields]), user["address"], workbook.add_format({
        'align': 'center',
        'valign': 'vcenter'
    }))
    worksheet.merge_range(
        'A6:{}6'.format(align[no_of_fields]), "Ph No. {} | Email - {}".format(user["phone"], user["email"]), workbook.add_format({
            'align': 'center',
            'valign': 'vcenter'
        }))
    border_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter'
    })
    border_format.set_bottom(1)
    worksheet.merge_range(
        'A7:{}7'.format(align[no_of_fields]), "Pan no. {} | SAC: {}|| GSTIN- {}".format(user["pan"], user["sac"], user["gst"]), border_format)


def setClientInfo(data, workbook, worksheet):
    headings = data['heading']
    client = data['client']
    border_left = workbook.add_format({})
    bold = workbook.add_format({'bold': True})
    border_left.set_left(1)
    align = {}
    for i in range(1, 27):
        align[i] = chr(i+64)
    no_of_fields = len(headings)

    client_name_format = workbook.add_format({
        'bold': True,
    })
    client_name_format.set_underline(1)
    worksheet.merge_range('A9:C9', client["name"], client_name_format)
    worksheet.merge_range('A10:C12', getPath(client["address"]))
    worksheet.write('A13', "CITY", bold)
    worksheet.write('B13', client["city"])
    worksheet.write('C13', "PINCODE : {}".format(client["pin"]), bold)
    # worksheet.write('D13', client["pin"])

    worksheet.write('{}9'.format(align[no_of_fields-1]), "GST No", bold)
    worksheet.write('{}9'.format(align[no_of_fields]), client["gst"], bold)

    worksheet.write('{}11'.format(align[no_of_fields-1]), "Mob No.", bold)
    worksheet.write('{}11'.format(align[no_of_fields]), client["mob"], bold)

    worksheet.write('{}12'.format(align[no_of_fields-1]), "Tel No.", bold)
    worksheet.write('{}12'.format(align[no_of_fields]), client["tel"], bold)

    worksheet.write('{}13'.format(align[no_of_fields-1]), "Email", bold)
    worksheet.write('{}13'.format(align[no_of_fields]), client["email"])

    for i in range(8, 16):
        worksheet.write('{}{}'.format(
            align[no_of_fields-2], i), "", border_left)


def setUserAndClientInfo(data,workbook,worksheet):
    setUserInfo(data,workbook,worksheet)
    setClientInfo(data,workbook,worksheet)

def number_to_word(number):
    def get_word(n):
        words = {0: "", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen",
                 15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen", 20: "Twenty", 30: "Thirty", 40: "Forty", 50: "Fifty", 60: "Sixty", 70: "Seventy", 80: "Eighty", 90: "Ninty"}
        if n <= 20:
            return words[n]
        else:
            ones = n % 10
            tens = n-ones
            return words[tens]+" "+words[ones]

    def get_all_word(n):
        d = [100, 10, 100, 100]
        v = ["", "Hundred And", "Thousand", "lakh"]
        w = []
        for i, x in zip(d, v):
            t = get_word(n % i)
            if t != "":
                t += " "+x
            w.append(t.rstrip(" "))
            n = n//i
        w.reverse()
        w = ' '.join(w).strip()
        if w.endswith("And"):
            w = w[:-3]
        return w

    arr = str(number).split(".")
    number = int(arr[0])
    crore = number//10000000
    number = number % 10000000
    word = ""
    if crore > 0:
        word += get_all_word(crore)
        word += " crore "
    word += get_all_word(number).strip()+" Rupees"
    if len(arr) > 1:
        if len(arr[1]) == 1:
            arr[1] += "0"
        word += " and "+get_all_word(int(arr[1]))+" paisa"
    return word


def getPath(text):

    length = len(text)
    abhiTakLength = startP = prevPos = no = 0
    breakP = maxWidth = 30
    textToBeDisplayedList = []
    if(length<breakP):
       return text
    while (abhiTakLength < length):
        no += 1
        for i in range(breakP, startP, -1):
            if (text[i] == ' ' and breakP != length-1):
                prevPos = i
                break
            else:
                prevPos = length
        breakP = prevPos + 1
        textToBeDisplayed = text[startP:prevPos+1]
        startP = breakP
        breakP = startP + maxWidth
        if (breakP >= length):
            breakP = length - 1
        abhiTakLength += len(textToBeDisplayed)
        textToBeDisplayedList.append(textToBeDisplayed)
    toBeReturned = "\n".join(textToBeDisplayedList)
    return toBeReturned


def getBill(data,workbook):

    billHead = data['heading']
    bills = data['bills']
    user = data['user']
    worksheet = workbook.add_worksheet("Data")
    
    border_left = workbook.add_format({})
    bold = workbook.add_format({'bold': True})
    border_left.set_left(1)
    align = {}
    for i in range(1, 27):
        align[i] = chr(i+64)
    no_of_fields = len(billHead)


    # adding client and user details
    setUserAndClientInfo(data,workbook,worksheet)


    # adding data from here
    row = 15
    col = 0

    border_format = workbook.add_format({
        'align': 'left', 'bold': True,     'align': 'center',
        'valign': 'vcenter'
    })

    border_format.set_top(1)  # Set value to true
    border_format.set_bottom(1)  # Set value to true
    for fields in billHead:
        worksheet.write(row, col, (fields), border_format)
        worksheet.set_column('{0}:{0}'.format(align[col+1]), len(fields)+3)
        col += 1
        # if len(fields) > description_col_width:
        #     description_col_width = len(fields)



    worksheet.set_row(row, 30)
    worksheet.set_column("A:A", 12)

    col = 0
    row = 16
    startrow = 16
    total = 0
    for bill in (bills):
        col = 0
        for fields in bill:
            worksheet.write(row, col,   bill[fields])
            col += 1
        row += 1
        total += bill['amount']

    # to show sum
    sum_row = row + 1
    print(no_of_fields)
    worksheet.merge_range('A{0}:{1}{0}'.format(
        sum_row, align[no_of_fields-1]), "TOTAL AMOUNT")
    worksheet.write(row, no_of_fields-1, '=SUM({2}{0}:{2}{1})'.format(
        startrow+1, len(bills) + startrow, align[no_of_fields]), bold)

    # to show c.gst
    worksheet.write(sum_row,  no_of_fields-3, 'C.GST', border_left)
    worksheet.write_number(sum_row,  no_of_fields-2, 0.00)
    worksheet.write(sum_row,  no_of_fields-1, '={2}{0}*{3}{1}'.format(
        sum_row, sum_row+1, align[no_of_fields], align[no_of_fields-1]))

    # to show s.gst
    worksheet.write(sum_row+1,  no_of_fields-3, 'S.GST', border_left)
    worksheet.write_number(sum_row+1,  no_of_fields-2, 0.00)
    # worksheet.write(sum_row+1,  no_of_fields-1, '=H{}*G{}'.format(sum_row, sum_row+2))
    worksheet.write(sum_row+1,  no_of_fields-1, '={2}{0}*{3}{1}'.format(
        sum_row, sum_row+2, align[no_of_fields], align[no_of_fields-1]))

    # to show I.gst
    worksheet.write(sum_row+2,  no_of_fields-3, 'I.GST', border_left)
    worksheet.write_number(sum_row+2,  no_of_fields-2, 0.05)
    # worksheet.write(sum_row+2,  no_of_fields-1, '=H{}*G{}'.format(sum_row, sum_row+3))
    worksheet.write(sum_row+2,  no_of_fields-1, '={2}{0}*{3}{1}'.format(
        sum_row, sum_row+3, align[no_of_fields], align[no_of_fields-1]))

    total = total*1.05
    # to write number in name format
    worksheet.merge_range('A{0}:{2}{1}'.format(
        sum_row+1, sum_row+3, align[no_of_fields-3]), "In Number format\nRuppess {}".format(number_to_word(total)), bold)

    border_format = workbook.add_format({
        'align': 'left', 'bold': True,     'align': 'center',
        'valign': 'vcenter'
    })

    border_format.set_bottom(1)

    # to show total bill
    worksheet.merge_range('A{0}:{1}{0}'.format(
        sum_row+4, align[no_of_fields-1]), "Total bill. Amt in Rs", border_format)
    worksheet.write(sum_row+3,  no_of_fields-1,
                    '=SUM({2}{0}:{2}{1})'.format(sum_row, sum_row+3, align[no_of_fields]), border_format)

    # adding bank details of user
    worksheet.merge_range('A{0}:D{0}'.format(
        sum_row+5), "BANK NAME           : {}".format(user["bank_name"]), bold)
    worksheet.merge_range('A{0}:D{0}'.format(
        sum_row+6), "BANK AC No.         : {}".format(user["bank_acno"]), bold)
    worksheet.merge_range('A{0}:D{0}'.format(
        sum_row+7), "BANK IFSC Code.    : {}".format(user["bank_ifsc"]), bold)


def compute_rows(text, width):
    if len(text) < width:
        return 1
    phrases = text.replace('\r', '').split('\n')
 
    rows = 0
    for phrase in phrases:
        if len(phrase) < width:
            rows = rows + 1
        else:
            words = phrase.split(' ')
            temp = ''
            for idx, word in enumerate(words):
                temp = temp + word + ' '
                # check if column width exceeded
                if len(temp) > width:
                    rows = rows + 1
                    temp = '' + word + ' '
                # check if it is not the last word
                if idx == len(words) - 1 and len(temp) > 0:
                    rows = rows + 1
    return rows

    
def getLedger(data,workbook):


    transHead = data['heading']
    trans = data['trans']
    worksheet = workbook.add_worksheet("Data")
    bold = workbook.add_format({'bold': True})
    underline = workbook.add_format({'underline': True})

    border_left = workbook.add_format({})
    border_left.set_left(1)
    align = {}
    for i in range(1, 27):
        align[i] = chr(i+64)
    no_of_fields = len(transHead)
    
    setUserAndClientInfo(data,workbook,worksheet)


    row = 15
    col = 0

    border_format = workbook.add_format({
        'align': 'left', 'bold': True,     'align': 'center',
        'valign': 'vcenter'
    })
    
    border_format.set_top(1)  # Set value to true
    border_format.set_bottom(1)  # Set value to true
    for fields in transHead:
        worksheet.write(row, col, (fields), border_format)
        worksheet.set_column('{0}:{0}'.format(align[col+1]), len(fields)+3)
        col += 1

    

    worksheet.set_row(row, 30)
    for i in range(no_of_fields):
        worksheet.set_column("{0}:{0}".format(align[i+1]), 12)

    col = 0
    row = 16
    startrow = 16
    total = 0
    for transaction in (trans):
        col = 0
        for fields in transaction:
            worksheet.write(row, col,   transaction[fields])
            col += 1
        row += 1


    border_format = workbook.add_format({
        # 'align': 'left', 'bold': True,     'align': 'center',
        # 'valign': 'vcenter'
    })
    border_format.set_top(1)
    for transaction in (trans):
        col = 0
        for fields in transaction:
            worksheet.write(row, col,"" , border_format)
            col += 1
        row += 1
        break
    startOf = 2

        
    balance = 0
    totDebit = 0
    totCredit = 0
    for transaction in trans:
        debit = transaction['debit']
        credit = transaction['credit']
        if(type(credit)==str):
            credit = 0
        if(type(debit)==str):
            debit = 0
        credit = float(credit)
        totCredit += credit
        balance += credit
        debit = float(debit)
        totDebit += debit
        balance -= debit


    worksheet.write(row, startOf, "TOTAL")
    worksheet.write(row, startOf+1, totDebit)
    worksheet.write(row, startOf + 2, totCredit)


    border_format_total = workbook.add_format({
        # 'align': 'left', 'bold': True,     'align': 'center',
        # 'valign': 'vcenter'
    })
    border_format_total.set_bottom(1)
    border_format_total.set_top(1)
    border_format_total.set_bold(True)
    if totDebit > totCredit:
        worksheet.write(row+1, startOf, "Debit Balance")
        worksheet.write(row+1, startOf+2, totDebit - totCredit)
        worksheet.write(row+2, startOf+1, totDebit,border_format_total)
        worksheet.write(row+2, startOf + 2, totDebit,border_format_total)
    else:
        worksheet.write(row+1, startOf, "Credit Balance")
        worksheet.write(row+1, startOf + 1,  totCredit - totDebit)
        worksheet.write(row+2, startOf+1, totCredit,border_format_total)
        worksheet.write(row+2, startOf + 2, totCredit,border_format_total)

    worksheet.write(row+2, startOf, "Grand Total")
    for i in range(no_of_fields):
        worksheet.set_column("{0}:{0}".format(align[i+1]), 12)
    worksheet.set_column("C:C", 25)


def getTrain(data,workbook):

    # fileName = data['filename']
    trainHead = data['heading']
    trains = data['trains']
    worksheet = workbook.add_worksheet("Data")
    bold = workbook.add_format({'bold': True})

    border_left = workbook.add_format({})
    border_left.set_left(1)
    align = {}
    for i in range(1, 27):
        align[i] = chr(i+64)
    no_of_fields = len(trainHead)

    setUserInfo(data, workbook, worksheet)

    row = 7
    col = 0

    border_format = workbook.add_format({
        'align': 'left', 'bold': True,     'align': 'center',
        'valign': 'vcenter'
    })

    border_format.set_top(1)  # Set value to true
    border_format.set_bottom(1)  # Set value to true
    for fields in trainHead:
        worksheet.write(row, col, (fields), border_format)
        worksheet.set_column('{0}:{0}'.format(align[col+1]), len(fields)+3)
        col += 1

    worksheet.set_row(row, 30)
    worksheet.set_column("A:A", 12)

    row += 1
    startOf  = startrow = row     
    
    previousDate = trains[0]['date']
    dateTotal = 0
    dataLength = 0
    for index, train in enumerate(trains):
        if(train["date"]==previousDate):
            dateTotal += train['amount']
            dataLength += 1
        else:
            trains[index-1]['amount_day'] = dateTotal
            trains[index-1]['pl_day'] =  dateTotal - train['mr_amount']
            trains[index-1]['dateLength'] =  dataLength
            dataLength = 1
            previousDate = train['date']
            dateTotal = train['amount']
    train = trains[len(trains) - 1 ]
    train['amount_day'] = dateTotal
    train['pl_day'] =  dateTotal - train['mr_amount']
    train['dateLength'] =  dataLength
    previousDate = train['date']
    dateTotal = train['amount']

    col = 0
    print(len(trains))
    for train in (trains):
        worksheet.write(row, col,     train["date"])
        worksheet.write(row, col+1,   train["gr_number"])
        worksheet.write(row, col+2,   train["party"])
        worksheet.write(row, col+3,   train["no_of_packages"])
        worksheet.write(row, col+4,   train["weight"])
        worksheet.write(row, col+5,   train["price_per_weight"])
        worksheet.write(row, col+6,   train["amount"])
        try : 

            dataLength = train['dateLength']
            print(dataLength)
            if(dataLength==1):
                worksheet.write(row, col+7,   train['amount_day'])
                worksheet.write(row, col+8,   train['mr_amount'])
                worksheet.write(row, col+9,   train['pl_day'],bold)
            else:
                # dataLength +=2 
                startrow = row + 1
                worksheet.merge_range('{0}{1}:{0}{2}'.format(align[no_of_fields-2],startrow +1- dataLength ,row+1), train['amount_day'])
                worksheet.merge_range('{0}{1}:{0}{2}'.format(align[no_of_fields-1],startrow +1- dataLength ,row+1), train['mr_amount'])
                worksheet.merge_range('{0}{1}:{0}{2}'.format(align[no_of_fields],startrow +1 - dataLength,row +1), train['pl_day'],bold)
            
        except Exception as e:
            print(e)
        row += 1

        # total += bill['amount']
    border_format = workbook.add_format({
    })
    border_format.set_top(1)
    # for train in (trains):
    col = 0
    for fields in trainHead:
        worksheet.write(row, col, "", border_format)
        col += 1
    row += 1

    border_format.set_top(1)
    border_format.set_bold(True)

    worksheet.write("{}{}".format(align[no_of_fields],row), "=SUM({0}{1}:{0}{2})".format(align[no_of_fields],startOf+1,row-1), border_format)
    worksheet.write("{}{}".format(align[no_of_fields -1 ],row), "Total P/L", border_format)


    for i in range(no_of_fields):
        worksheet.set_column("{0}:{0}".format(align[i+1]), 12)

