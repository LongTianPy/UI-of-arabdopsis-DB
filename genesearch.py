#! /usr/bin/python
#This is the script for gene name search
import cgi, MySQLdb, subprocess, os, random
os.environ['HOME']='c:\Apache\htdocs'
os.environ['MPLCONFIGDIR']='c:\Apache\htdocs'
import matplotlib
matplotlib.use('Agg')
import numpy
import matplotlib.pyplot as plt
import matplotlib.figure
import pylab



def process():
    form=cgi.FieldStorage()
    gfeature=form.getfirst('genename')
    gsearch=form.getfirst('gnsearch')
    if gsearch is None:
        gsearch=gsearch
    else:
        if ',' in gsearch:
            gsearch=gsearch.split(',')
        else:
            gsearch=[gsearch]
    expp1=form.getfirst('exp1')
    expsearch1=form.getfirst('expsearch1')
    expp2=form.getfirst('exp2')
    expsearch2=form.getfirst('expsearch2')
    expp3=form.getfirst('exp3')
    expsearch3=form.getfirst('expsearch3')
    filename='result.png'
    f=open('supercluster.txt','r')
    rows=[i.split('\t') for i in f.readlines()]
    f.close()
    if gsearch is None: #if nothing's input
        print 'Content-type: text/html'
        print 
        print '<html><head>'
        print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
        print '</head>'
        print '<body>'
        print '<form action="index.py">'
        print '<div id="topbanner">'
        print '<h1>Welcome to Arabidopsis Athaliana Microarray Database!</h1>'
        print '</div>'
        print '<div id="mainbody">'
        print '<table>'
        print '<tbody>'
        print '<tr><td>'
        print '<h2>Please do not leave the query area blank</h2>'
        print '</td></tr>'
        print '<tr><td><input type="submit" value="Try again"></td></tr>'
        print '</tbody>'
        print '</table>'
        print '</div>'
        print '</form>'
        print '</body>'
        print '</html>'
    else:
        db=MySQLdb.connect(host="localhost",user='root',passwd='')
        c=db.cursor()
        c.execute('use athaliana')
        dataid_probeid=[]
        dataid_exp=[]
        result_gene=[]
        result_exp=[]
        result_value=[]
        if gfeature=="1":#if doing probe is searched, whole rows of exression data are returned
            for i in gsearch:
                c.execute('select DataID from Data use index (dataindex) where DataName="%s"'%i)
                temp=c.fetchone()
                if len(temp)!=0:
                    dataid_probeid.append(temp[0])
            for i in dataid_probeid:
                c.execute('select DataName from Data use index (dataidindex) where DataID="%s"'%i)
                temp=c.fetchone()
                if len(temp)!=0:
                    result_gene.append(temp[0])
            if expp1 =="1" and expp2 =="1" and expp3 == "1":
                for i in dataid_probeid:
                    value_temp=rows[(int(i)-1)]
                    result_value.append(value_temp)
                c.execute('select DataName from Data where DTypeID=2')
                result_exp=c.fetchall()
                db.commit()
                #plot                
                for i in range(len(dataid_probeid)):
                    plt.subplot(len(dataid_probeid),1,(i+1))
                    matplotlib.figure.Figure(figsize=(12,6))
                    plt.plot(result_value[i])
                    plt.axhline(y=0,color='r',linewidth=1)
                    plt.ylabel('Expression level')
                    plt.title('Gene expression level for %s'%result_gene[i])
                    plt.xticks(numpy.arange(len(result_value[i])),['']*len(result_value[i]))
                    
                    
                os.chdir("c:\Apache\htdocs")
                pylab.savefig(filename,format="png")
                os.chdir('c:\Apache\htdocs')
                os.system('del result.txt')
                os.system('type NUL > result.txt')
                line_exp=[str(i)[2:-3] for i in result_exp]
                line_gene=[str(i) for i in result_gene]
                header=['ProbeID']+line_exp
                f=open('result.txt','a')
                f.writelines('\t'.join(header))
                for i in range(len(line_gene)):
                    for j in range(len(result_value[i])):
                        if result_value[i][j]=='-50':
                            result_value[i][j]=='N/A'
                    lines=[line_gene[i]]+result_value[i]
                    lines=[str(j) for j in lines]
                    f.writelines('\t'.join(lines))
                f.close()
                
                print 'Content-type: text/html'
                print 
                print '''<html><head>'''
                print '''<title>Arabdopsis Athaliana Microarray Data Browser</title>'''
                print '''</head>'''
                print '''<body>'''
                print '''<form action="index.py">'''
                print '''<div id="topbanner">'''
                print '''<h1>Here are your results</h1>'''
                print '''<h2>Or, you may re-modify your search</h2>'''
                print '''<input type="submit" value="Try again">'''
                print '<h3>For downloadable text file, right click on the following link and select "Save link as..."</h3>'
                print '<a href="/result.txt" target="_blank">Download</a>'
                print ''
                print '<h4>For genes whose values are not available, "-50" is plotted on the graphs to mark them, and it shows "N/A" in the downloadable file.</h4>'
                print '''</div>'''
                print '''</form>'''
                print '''<div id="mainbody">'''
                print '''<table border="1">'''
                print '''<tbody>'''
                print '''<tr><td width="500px"><b>Probe ID</b></td>'''
                for i in result_exp:
                    print '<td width="500px">'
                    print '<a href="expsearch.py?expname=%s">'%i[0]
                    print '<b>%s</b></a></td>'%i[0]
                print '''</tr>'''
                for i in range(len(result_gene)):
                    print '''<tr><td width="500px"><a href="gene.py?genename=%s" target="_blank">%s</td>'''%(result_gene[i],result_gene[i])
                    for j in range(len(result_exp)):
                        print '''<td width="500px">%s</td>'''%result_value[i][j]
                    print '''</tr>'''
                print '''</tbody>'''
                print '''</table>'''
                print '''</div>'''
                print '''<div>'''
                print ''
                print ''
                print '<img src="/%s"></img>'%filename
                print '''</div>'''
                print '''</body>'''
                print '''</html>'''
            else:
                if expp1=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch1+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                elif expp1=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch1+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                elif expp1=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch1.upper()+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                if expp2=="1":
                    id_exp2=()
                elif expp2=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch2+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                elif expp2=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch2+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                elif expp2=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch2.upper()+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                if expp3=="1":
                    id_exp3=()
                elif expp3=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch3+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                elif expp3=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch3+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                elif expp3=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch3.upper()+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                id_exp=id_exp1+id_exp2+id_exp3
                id_exp=set(id_exp)
                id_exp=list(id_exp)
                if len(id_exp)!=0:
                    result_value=[]
                    for i in id_exp:
                        c.execute('select DataName from Data use index (dataidindex) where DataID="%s" and DTypeID=2'%i)
                        temp=c.fetchone()
                        result_exp.append(temp[0])
                    id_exp=[i-22810-1 for i in id_exp]
                    for i in dataid_probeid:
                        temp_pergene=[]
                        temp=numpy.array(rows[(int(i)-1)])
                        temp=list(temp[id_exp])
                        result_value.append(temp)
                    db.commit()
                    for i in range(len(dataid_probeid)):
                        plt.subplot(len(dataid_probeid),1,(i+1))
                        matplotlib.figure.Figure(figsize=(12,6))
                        plt.plot(result_value[i])
                        plt.axhline(y=0,color='r',linewidth=1)
                        plt.ylabel('Expression level')
                        plt.title('Gene expression level for %s'%result_gene[i])
                        plt.xticks(numpy.arange(len(result_value[i])),['']*len(result_value[i]))
                        
                        
                        
                    os.chdir("c:\Apache\htdocs")
                    pylab.savefig(filename,format="png")
                    os.chdir('c:\Apache\htdocs')
                    os.system('del result.txt')
                    os.system('type NUL > result.txt')
                    line_exp=[str(i)[2:-3] for i in result_exp]
                    line_gene=[str(i) for i in result_gene]
                    header=['ProbeID']+line_exp
                    f=open('result.txt','a')
                    f.writelines('\t'.join(header))
                    for i in range(len(line_gene)):
                        for j in range(len(result_value[i])):
                            if result_value[i][j]=='-50':
                                result_value[i][j]=='N/A'                        
                        lines=[line_gene[i]]+result_value[i]
                        lines=[str(j) for j in lines]
                        f.writelines('\t'.join(lines))
                    f.close()

                    print 'Content-type: text/html'
                    print 
                    print '<html><head>'
                    print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
                    print '</head>'
                    print '<body>'
                    print '<div id="topbanner">'
                    print '<form action="index.py">'
                    print '<h1>Here are your results</h1>'
                    print '<h2>Or, you may re-modify your search</h2>'
                    print '<input type="submit" value="Try again">'
                    print '<h3>For downloadable text file, right click on the following link and select "Save link as..."</h3>'
                    print '<a href="/result.txt" target="_blank">Download</a>'
                    print ''
                    print '<h4>For genes whose values are not available, "-50" is plotted on the graphs to mark them, and it shows "N/A" in the downloadable file.</h4>'

                    print '</form>'
                    print '</div>'
                    print '<div id="mainbody">'
                    print '<table border="1">'
                    print '<tbody>'
                    print '<tr><td width="500px"><b>Probe ID</b></td>'
                    for i in result_exp:
                        print '<td width="500px">'
                        print '<a href="expsearch.py?expname=%s">'%i
                        print '<b>%s</b></a></td>'%i
                    print '''</tr>'''
                    for i in range(len(result_gene)):
                        print '''<tr><td width="500px"><a href="gene.py?genename=%s" target="_blank">%s</td>'''%(result_gene[i],result_gene[i])
                        for j in range(len(result_exp)):
                            print '''<td width="500px">%s</td>'''%result_value[i][j]
                        print '''</tr>'''
                    print '</tbody>'
                    print '</table>'
                    print '</div>'
                    print '''<div>'''
                    print ''
                    print ''
                    print '<img src="/%s"></img>'%filename
                    print '''</div>'''
                    print '</body>'
                    print '</html>'
                else:
                    print 'Content-type: text/html'
                    print 
                    print '<html><head>'
                    print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
                    print '</head>'
                    print '<body>'
                    print '<div id="topbanner">'
                    print '<form action="index.py">'
                    print '<h1>Here are your results</h1>'
                    print '<h2>Or, you may re-modify your search</h2>'
                    print '<input type="submit" value="Try again">'
                    print '</form>'
                    print '</div>'
                    print '<div id="mainbody">'
                    print '<table width="800px">'
                    print '<tbody>'
                    print '<tr><td>No result found</td></tr>'
                    print '</tbody>'
                    print '</table>'
                    print '</div>'                   
                    print '</body>'
                    print '</html>'

        if gfeature=="2":#if doing gene symbol search
            for i in gsearch:
                c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=1 and DAValue="%s"'%i.upper())
                temp=c.fetchone()
                if len(temp)!=0:
                    dataid_probeid.append(temp[0])
            for i in dataid_probeid:
                c.execute('select DataName from Data use index (dataidindex) where DataID="%s"'%i)
                temp=c.fetchone()
                if len(temp)!=0:
                    result_gene.append(temp[0])
            if expp1 =="1" and expp2 =="1" and expp3 == "1":
                for i in dataid_probeid:
                    value_temp=rows[(int(i)-1)]
                    result_value.append(value_temp)
                c.execute('select DataName from Data where DTypeID=2')
                result_exp=c.fetchall()
                db.commit()
                #plot                
                for i in range(len(dataid_probeid)):
                    plt.subplot(len(dataid_probeid),1,(i+1))
                    matplotlib.figure.Figure(figsize=(12,6))
                    plt.plot(result_value[i])
                    plt.axhline(y=0,color='r',linewidth=1)
                    plt.ylabel('Expression level')
                    plt.title('Gene expression level for %s'%result_gene[i])
                    plt.xticks(numpy.arange(len(result_value[i])),['']*len(result_value[i]))
                   
                    
                    
                os.chdir("c:\Apache\htdocs")
                pylab.savefig(filename,format="png")
                os.chdir('c:\Apache\htdocs')
                os.system('del result.txt')
                os.system('type NUL > result.txt')
                line_exp=[str(i)[2:-3] for i in result_exp]
                line_gene=[str(i) for i in result_gene]
                header=['ProbeID']+line_exp
                f=open('result.txt','a')
                f.writelines('\t'.join(header))
                for i in range(len(line_gene)):
                    for j in range(len(result_value[i])):
                        if result_value[i][j]=='-50':
                            result_value[i][j]=='N/A'                    
                    lines=[line_gene[i]]+result_value[i]
                    lines=[str(j) for j in lines]
                    f.writelines('\t'.join(lines))
                f.close()

                db.commit()
                print 'Content-type: text/html'
                print 
                print '''<html><head>'''
                print '''<title>Arabdopsis Athaliana Microarray Data Browser</title>'''
                print '''</head>'''
                print '''<body>'''
                print '''<form action="index.py">'''
                print '''<div id="topbanner">'''
                print '''<h1>Here are your results</h1>'''
                print '''<h2>Or, you may re-modify your search</h2>'''
                print '''<input type="submit" value="Try again">'''
                print '<h3>For downloadable text file, right click on the following link and select "Save link as..."</h3>'
                print '<a href="/result.txt" target="_blank">Download</a>'
                print ''
                print '<h4>For genes whose values are not available, "-50" is plotted on the graphs to mark them, and it shows "N/A" in the downloadable file.</h4>'

                print '''</div>'''
                print '''<div id="mainbody">'''
                print '''<table border="1">'''
                print '''<tbody>'''
                print '''<tr><td width="500px"><b>Probe ID</b></td>'''
                for i in result_exp:
                    print '<td width="500px">'
                    print '<a href="expsearch.py?expname=%s">'%i[0]
                    print '<b>%s</b></a></td>'%i[0]
                print '''</tr>'''
                for i in range(len(result_gene)):
                    print '''<tr><td width="500px"><a href="gene.py?genename=%s" target="_blank">%s</td>'''%(result_gene[i],result_gene[i])
                    for j in range(len(result_exp)):
                        print '''<td width="500px">%s</td>'''%result_value[i][j]
                    print '''</tr>'''
                print '''</tbody>'''
                print '''</table>'''
                print '''</div>'''
                print '''<div>'''
                print ''
                print ''
                print '<img src="/%s"></img>'%filename
                print '</div>'
                print '''</form>'''
                print '''</body>'''
                print '''</html>'''
            else:
                if expp1=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch1+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                elif expp1=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch1+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                elif expp1=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch1.upper()+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                if expp2=="1":
                    id_exp2=()
                elif expp2=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch2+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                elif expp2=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch2+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                elif expp2=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch2.upper()+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                if expp3=="1":
                    id_exp3=()
                elif expp3=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch3+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                elif expp3=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch3+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                elif expp3=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch3.upper()+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                id_exp=id_exp1+id_exp2+id_exp3
                id_exp=set(id_exp)
                id_exp=list(id_exp)
                if len(id_exp)!=0:
                    result_value=[]
                    for i in id_exp:
                        c.execute('select DataName from Data use index (dataidindex) where DataID="%s"'%i)
                        temp=c.fetchone()
                        result_exp.append(temp[0])
                    id_exp=[i-22810-1 for i in id_exp]
                    for i in dataid_probeid:
                        temp_pergene=[]
                        temp=numpy.array(rows[(int(i)-1)])
                        temp=list(temp[id_exp])
                        result_value.append(temp)
                    db.commit()
                    for i in range(len(dataid_probeid)):
                        plt.subplot(len(dataid_probeid),1,(i+1))
                        matplotlib.figure.Figure(figsize=(12,6))
                        plt.plot(result_value[i])
                        plt.axhline(y=0,color='r',linewidth=1)
                        plt.ylabel('Expression level')
                        plt.title('Gene expression level for %s'%result_gene[i])
                        plt.xticks(numpy.arange(len(result_value[i])),['']*len(result_value[i]))
                        
                    os.chdir("c:\Apache\htdocs")
                    pylab.savefig(filename,format="png")
                    os.chdir('c:\Apache\htdocs')
                    os.system('del result.txt')
                    os.system('type NUL > result.txt')
                    line_exp=[str(i)[2:-3] for i in result_exp]
                    line_gene=[str(i) for i in result_gene]
                    header=['ProbeID']+line_exp
                    f=open('result.txt','a')
                    f.writelines('\t'.join(header))
                    for i in range(len(line_gene)):
                        for j in range(len(result_value[i])):
                            if result_value[i][j]=='-50':
                                result_value[i][j]=='N/A'
                        lines=[line_gene[i]]+result_value[i]
                        lines=[str(j) for j in lines]
                        f.writelines('\t'.join(lines))
                    f.close()

                    print 'Content-type: text/html'
                    print 
                    print '<html><head>'
                    print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
                    print '</head>'
                    print '<body>'
                    print '<div id="topbanner">'
                    print '<form action="index.py">'
                    print '<h1>Here are your results</h1>'
                    print '<h2>Or, you may re-modify your search</h2>'
                    print '<input type="submit" value="Try again">'
                    print '</form>'
                    print '<h3>For downloadable text file, right click on the following link and select "Save link as..."</h3>'
                    print '<a href="/result.txt" target="_blank">Download</a>'
                    print ''
                    print '<h4>For genes whose values are not available, "-50" is plotted on the graphs to mark them, and it shows "N/A" in the downloadable file.</h4>'

                    print '</div>'
                    print '<div id="mainbody">'
                    print '<table border="1">'
                    print '<tbody>'
                    print '<tr><td width="500px"><b>Probe ID</b></td>'
                    for i in result_exp:
                        print '<td width="500px">'
                        print '<a href="expsearch.py?expname=%s">'%i
                        print '<b>%s</b></a></td>'%i
                    print '''</tr>'''
                    for i in range(len(result_gene)):
                        print '''<tr><td width="500px"><a href="gene.py?genename=%s" target="_blank">%s</td>'''%(result_gene[i],result_gene[i])
                        for j in range(len(result_exp)):
                            print '''<td width="500px">%s</td>'''%result_value[i][j]
                        print '''</tr>'''
                    print '</tbody>'
                    print '</table>'
                    print '</div>'
                    print '''<div>'''
                    print ''
                    print ''
                    print '<img src="/%s"></img>'%filename
                    print '</div>'
                    print '</body>'
                    print '</html>'
                else:
                    print 'Content-type: text/html'
                    print 
                    print '<html><head>'
                    print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
                    print '</head>'
                    print '<body>'
                    print '<div id="topbanner">'
                    print '<form action="index.py">'
                    print '<h1>Here are your results</h1>'
                    print '<h2>Or, you may re-modify your search</h2>'
                    print '<input type="submit" value="Try again">'
                    print '</form>'
                    print '</div>'
                    print '<div id="mainbody">'
                    print '<table width="800px">'
                    print '<tbody>'
                    print '<tr><td>No result found</td></tr>'
                    print '</tbody>'
                    print '</table>'
                    print '</div>'
                    print '</body>'
                    print '</html>'

        if gfeature=="3":
            for i in gsearch:
                c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=10 and DAValue like "%s"'%('%'+i.upper()+'%'))
                temp=c.fetchone()
                if len(temp)!=0:
                    dataid_probeid.append(temp[0])
            for i in dataid_probeid:
                c.execute('select DataName from Data use index (dataidindex) where DataID="%s"'%i)
                temp=c.fetchone()
                if len(temp)!=0:
                    result_gene.append(temp[0])
            if expp1 =="1" and expp2 =="1" and expp3 == "1":
                value_temp=rows[(int(i)-1)]
                result_value.append(value_temp)
                c.execute('select DataName from Data where DTypeID=2')
                result_exp=c.fetchall()
                db.commit()
                for i in range(len(dataid_probeid)):
                    plt.subplot(len(dataid_probeid),1,(i+1))
                    matplotlib.figure.Figure(figsize=(12,6))
                    plt.plot(result_value[i])
                    plt.axhline(y=0,color='r',linewidth=1)
                    plt.ylabel('Expression level')
                    plt.title('Gene expression level for %s'%result_gene[i])
                    plt.xticks(numpy.arange(len(result_value[i])),['']*len(result_value[i]))
                
                    

                os.chdir("c:\Apache\htdocs")
                pylab.savefig(filename,format="png")
                os.chdir('c:\Apache\htdocs')
                os.system('del result.txt')
                os.system('type NUL > result.txt')
                line_exp=[str(i)[2:-3] for i in result_exp]
                line_gene=[str(i) for i in result_gene]
                header=['ProbeID']+line_exp
                f=open('result.txt','a')
                f.writelines('\t'.join(header))
                for i in range(len(line_gene)):
                    for j in range(len(result_value[i])):
                        if result_value[i][j]=='-50':
                            result_value[i][j]=='N/A'
                    lines=[line_gene[i]]+result_value[i]
                    lines=[str(j) for j in lines]
                    f.writelines('\t'.join(lines))
                f.close()

                print 'Content-type: text/html'
                print 
                print '''<html><head>'''
                print '''<title>Arabdopsis Athaliana Microarray Data Browser</title>'''
                print '''</head>'''
                print '''<body>'''
                print '''<form action="index.py">'''
                print '''<div id="topbanner">'''
                print '''<h1>Here are your results</h1>'''
                print '''<h2>Or, you may re-modify your search</h2>'''
                print '''<input type="submit" value="Try again">'''
                print '<h3>For downloadable text file, right click on the following link and select "Save link as..."</h3>'
                print '<a href="/result.txt" target="_blank">Download</a>'
                print ''
                print '<h4>For genes whose values are not available, "-50" is plotted on the graphs to mark them, and it shows "N/A" in the downloadable file.</h4>'

                print '''</div>'''
                print '''<div id="mainbody">'''
                print '''<table border="1">'''
                print '''<tbody>'''
                print '''<tr><td width="500px"><b>Probe ID</b></td>'''
                for i in result_exp:
                    print '<td width="500px">'
                    print '<a href="expsearch.py?expname=%s">'%i[0]
                    print '<b>%s</b></a></td>'%i[0]
                print '''</tr>'''
                for i in range(len(result_gene)):
                    print '''<tr><td width="500px"><a href="gene.py?genename=%s" target="_blank">%s</td>'''%(result_gene[i],result_gene[i])
                    for j in range(len(result_exp)):
                        print '''<td width="500px">%s</td>'''%result_value[i][j]
                    print '''</tr>'''
                print '''</tbody>'''
                print '''</table>'''
                print '''</div>'''
                print '''<div>'''
                print ''
                print ''
                print '<img src="/%s"></img>'%filename
                print '</div>'
                print '''</form>'''
                print '''</body>'''
                print '''</html>'''
            else:
                if expp1=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch1+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                elif expp1=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch1+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                elif expp1=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch1.upper()+'%'))
                    temp=c.fetchall()
                    id_exp1=[i[0] for i in temp]
                    id_exp1=tuple(id_exp1)
                if expp2=="1":
                    id_exp2=()
                elif expp2=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch2+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                elif expp2=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch2+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                elif expp2=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch2.upper()+'%'))
                    temp=c.fetchall()
                    id_exp2=[i[0] for i in temp]
                    id_exp2=tuple(id_exp2)
                if expp3=="1":
                    id_exp3=()
                elif expp3=="2":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch3+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                elif expp3=="3":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch3+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                elif expp3=="4":
                    c.execute('select DataID from DAttribute use index (daindex, daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch3.upper()+'%'))
                    temp=c.fetchall()
                    id_exp3=[i[0] for i in temp]
                    id_exp3=tuple(id_exp3)
                id_exp=id_exp1+id_exp2+id_exp3
                id_exp=set(id_exp)
                id_exp=list(id_exp)
                if len(id_exp)!=0:
                    result_value=[]
                    for i in id_exp:
                        c.execute('select DataName from Data use index (dataidindex) where DataID="%s"'%i)
                        temp=c.fetchone()
                        result_exp.append(temp[0])
                    id_exp=[i-22810-1 for i in id_exp]
                    for i in dataid_probeid:
                        temp_pergene=[]
                        temp=numpy.array(rows[(int(i)-1)])
                        temp=list(temp[id_exp])
                        result_value.append(temp)
                    db.commit()
                    for i in range(len(dataid_probeid)):
                        plt.subplot(len(dataid_probeid),1,(i+1))
                        matplotlib.figure.Figure(figsize=(12,6))
                        plt.plot(result_value[i])
                        plt.axhline(y=0,color='r',linewidth=1)
                        plt.ylabel('Expression level')
                        plt.title('Gene expression level for %s'%result_gene[i])
                        plt.xticks(numpy.arange(len(result_value[i])),['']*len(result_value[i]))
                  
                        

                    os.chdir("c:\Apache\htdocs")
                    pylab.savefig(filename,format="png")
                    os.chdir('c:\Apache\htdocs')
                    os.system('del result.txt')
                    os.system('type NUL > result.txt')
                    line_exp=[str(i)[2:-3] for i in result_exp]
                    line_gene=[str(i) for i in result_gene]
                    header=['ProbeID']+line_exp
                    f=open('result.txt','a')
                    f.writelines('\t'.join(header))
                    for i in range(len(line_gene)):
                        for j in range(len(result_value[i])):
                            if result_value[i][j]=='-50':
                                result_value[i][j]=='N/A'
                        lines=[line_gene[i]]+result_value[i]
                        lines=[str(j) for j in lines]
                        f.writelines('\t'.join(lines))
                    f.close()

                    print 'Content-type: text/html'
                    print 
                    print '<html><head>'
                    print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
                    print '</head>'
                    print '<body>'
                    print '<div id="topbanner">'
                    print '<form action="index.py">'
                    print '<h1>Here are your results</h1>'
                    print '<h2>Or, you may re-modify your search</h2>'
                    print '<input type="submit" value="Try again">'
                    print '<h3>For downloadable text file, right click on the following link and select "Save link as..."</h3>'
                    print '<a href="/result.txt" target="_blank">Download</a>'
                    print ''
                    print '<h4>For genes whose values are not available, "-50" is plotted on the graphs to mark them, and it shows "N/A" in the downloadable file.</h4>'

                    print '</form>'
                    print '</div>'
                    print '<div id="mainbody">'
                    print '<table border="1">'
                    print '<tbody>'
                    print '<tr><td width="500px"><b>Probe ID</b></td>'
                    for i in result_exp:
                        print '<td width="500px">'
                        print '<a href="expsearch.py?expname=%s">'%i
                        print '<b>%s</b></a></td>'%i
                    print '''</tr>'''
                    for i in range(len(result_gene)):
                        print '''<tr><td width="500px"><a href="gene.py?genename=%s" target="_blank">%s</td>'''%(result_gene[i],result_gene[i])
                        for j in range(len(result_exp)):
                            print '''<td width="500px">%s</td>'''%result_value[i][j]
                        print '''</tr>'''
                    print '</tbody>'
                    print '</table>'
                    print '</div>'
                    print '''<div>'''
                    print ''
                    print ''
                    print '<img src="/%s"></img>'%filename
                    print '</div>'
                    print '</body>'
                    print '</html>'
                else:
                    print 'Content-type: text/html'
                    print 
                    print '<html><head>'
                    print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
                    print '</head>'
                    print '<body>'
                    print '<div id="topbanner">'
                    print '<form action="index.py">'
                    print '<h1>Here are your results</h1>'
                    print '<h2>Or, you may re-modify your search</h2>'
                    print '<input type="submit" value="Try again">'
                    print '</form>'
                    print '</div>'
                    print '<div id="mainbody">'
                    print '<table width="800px">'
                    print '<tbody>'
                    print '<tr><td>No result found</td></tr>'
                    print '</tbody>'
                    print '</table>'
                    print '</div>'
                    print '</body>'
                    print '</html>'



if __name__=="__main__":
    process()
                    
                
                
                
             
                
                
                
                            

                        
                
                        
                        
                        
                        
