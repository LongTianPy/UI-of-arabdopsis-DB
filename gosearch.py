#! c:/Python27/python.exe
#This is the script for GO term search
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
    go1=form.getfirst('genefunction1')
    gosearch1=form.getfirst('gfsearch1')
    go2=form.getfirst('genefunction2')
    gosearch2=form.getfirst('gfsearch2')
    go3=form.getfirst('genefunction3')
    gosearch3=form.getfirst('gfsearch3')
    exp1=form.getvalue('exp1')
    expsearch1=form.getfirst('expsearch1')
    exp2=form.getvalue('exp2')
    expsearch2=form.getfirst('expsearch2')
    exp3=form.getvalue('exp3')
    expsearch3=form.getfirst('expsearch3')
    filename='result.png'
    f=open('supercluster.txt','r')
    rows=[i.split('\t') for i in f.readlines()]
    f.close()
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j]=float(rows[i][j])
    if go1=="1" and go2=="1" and go3=="1" and exp1=="1" and exp2=="1" and exp3 == "1":
        print 'Content-type: text/html'
        print 
        print '<html><head>'
        print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
        print '</head>'
        print '<body>'
        print '<form action="ath.html">'
        print '<div id="topbanner">'
        print '<h1>Welcome to Arabidopsis Athaliana Microarray Database!</h1>'
        print '</div>'
        print '<div id="mainbody">'
        print '<table cellpadding=5 style="border-color:black;border-style:solid;border-width:thin" width="1000" align="center">'
        print '<tbody>'
        print '<tr><td>'
        print '<h2>Please do not leave the query area blank</h2>'
        print '</td></tr>'
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
        id_gene=[]
        dataid_exp=[]
        result_gene=[]
        result_exp=[]
        result_value=[]
        if go1=="1":
            id_gene1=()
        elif go1=="2":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) use index (daindex,daindex_id) where DATypeID=3 and DAValue like "%s"'%('%'+gosearch1+'%'))
            temp=c.fetchall()
            id_gene1=[i[0] for i in temp]
            id_gene1=tuple(id_gene1)
        elif go1=="3":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=4 and DAValue="%s"'%('%'+gosearch1+'%'))
            temp=c.fetchall()
            id_gene1=[i[0] for i in temp]
            id_gene1=tuple(id_gene1)
        elif go1=="4":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=5 and DAValue="%s"'%('%'+gosearch1+'%'))
            temp=c.fetchall()
            id_gene1=[i[0] for i in temp]
            id_gene1=tuple(id_gene1)
        if go2=="1":
            id_gene2=()
        elif go2=="2":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=3 and DAValue="%s"'%('%'+gosearch2+'%'))
            temp=c.fetchall()
            id_gene2=[i[0] for i in temp]
            id_gene2=tuple(id_gene2)
        elif go2=="3":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=4 and DAValue="%s"'%('%'+gosearch2+'%'))
            temp=c.fetchall()
            id_gene2=[i[0] for i in temp]
            id_gene2=tuple(id_gene2)
        elif go2=="4":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=5 and DAValue="%s"'%('%'+gosearch2+'%'))
            temp=c.fetchall()
            id_gene2=[i[0] for i in temp]
            id_gene2=tuple(id_gene2)
        if go3=="1":
            id_gene3=()
        elif go3=="2":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=3 and DAValue="%s"'%('%'+gosearch3+'%'))
            temp=c.fetchall()
            id_gene3=[i[0] for i in temp]
            id_gene3=tuple(id_gene3)
        elif go3=="3":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=4 and DAValue="%s"'%('%'+gosearch3+'%'))
            temp=c.fetchall()
            id_gene3=[i[0] for i in temp]
            id_gene3=tuple(id_gene3)
        elif go3=="4":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=5 and DAValue="%s"'%('%'+gosearch3+'%'))
            temp=c.fetchall()
            id_gene3=[i[0] for i in temp]
            id_gene3=tuple(id_gene3)
        id_gene=id_gene1+id_gene2+id_gene3
        id_gene=set(id_gene)
        id_gene=list(id_gene)
        if go1=="1" and go2=="1" and go3=="1" and (exp1!=1 or exp2!=1 or exp3!=1):
            c.execute('select DataID from Data where DTypeID=1')
            temp=c.fetchall()
            id_gene=[i[0] for i in temp]
        for i in id_gene:
            c.execute('select DataName from Data use index (dataidindex) where DataID="%s"'%i)
            result_gene.append(c.fetchall()[0][0])
        if exp1=="1":
            id_exp1=()
        elif exp1=="2":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch1+'%'))
            temp=c.fetchall()
            id_exp1=[i[0] for i in temp]
            id_exp1=tuple(id_exp1)
        elif exp1=="3":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch1+'%'))
            temp=c.fetchall()
            id_exp1=[i[0] for i in temp]
            id_exp1=tuple(id_exp1)
        elif exp1=="4":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch1.upper()+'%'))
            temp=c.fetchall()
            id_exp1=[i[0] for i in temp]
            id_exp1=tuple(id_exp1)
        if exp2=="1":
            id_exp2=()
        elif exp2=="2":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch2+'%'))
            temp=c.fetchall()
            id_exp2=[i[0] for i in temp]
            id_exp2=tuple(id_exp2)
        elif exp2=="3":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch2+'%'))
            temp=c.fetchall()
            id_exp2=[i[0] for i in temp]
            id_exp2=tuple(id_exp2)
        elif exp2=="4":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch2.upper()+'%'))
            temp=c.fetchall()
            id_exp2=[i[0] for i in temp]
            id_exp2=tuple(id_exp2)
        if exp3=="1":
            id_exp3=()
        elif exp3=="2":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=6 and DAValue like "%s"'%('%'+expsearch3+'%'))
            temp=c.fetchall()
            id_exp3=[i[0] for i in temp]
            id_exp3=tuple(id_exp3)
        elif exp3=="3":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=7 and DAValue like "%s"'%('%'+expsearch3+'%'))
            temp=c.fetchall()
            id_exp3=[i[0] for i in temp]
            id_exp3=tuple(id_exp3)
        elif exp3=="4":
            c.execute('select DataID from DAttribute use index (daindex,daindex_id) where DATypeID=9 and DAValue like "%s"'%('%'+expsearch3.upper()+'%'))
            temp=c.fetchall()
            id_exp3=[i[0] for i in temp]
            id_exp3=tuple(id_exp3)
        id_exp=id_exp1+id_exp2+id_exp3
        id_exp=set(id_exp)
        id_exp=list(id_exp)
        if exp1=="1" and exp2=="1" and exp3=="1" and (go1!="1" or gp2!="1" or go3!="1"):
            c.execute('select DataID from Data where DTypeID=2')
            temp=c.fetchall()
            id_exp=[i[0] for i in temp]
        for i in id_exp:
            c.execute('select DataName from Data use index (dataidindex) where DataID="%s"'%i)
            temp=c.fetchall()
            result_exp.append(temp[0])
        id_exp=[i-22810-1 for i in id_exp]
        if len(result_gene)!=0:
            for i in id_gene:
                temp_pergene=[]
                temp=numpy.array(rows[(int(i)-1)])
                temp=list(temp[id_exp])
                result_value.append(temp)
            db.commit()


            
            os.chdir('c:\Apache\htdocs')

            os.system('del result.txt')
            os.system('type NUL > result.txt')
            line_exp=[str(i)[2:-3] for i in result_exp]
            line_gene=[str(i) for i in result_gene]
            header=['ProbeID']+line_exp
            f=open('result.txt','a')
            f.writelines(header)
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
            print '</div>'
            print '<div id="mainbody">'
            print '<table border="1">'
            print '<tbody>'
            print '<tr><td width="500px"><b>Probe ID</b></td>'
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
            print '</tbody>'
            print '</table>'
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
            print '<form action="ath.htm">'
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
            
            
            
