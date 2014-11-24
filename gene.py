#! c:\Python27\python.exe
import os, cgi, MySQLdb

def main():
    form=cgi.FieldStorage()
    gene=form.getfirst('genename')
    db=MySQLdb.connect(host="localhost",user="root",passwd="")
    c=db.cursor()
    c.execute('use athaliana')
    c.execute('select DataID from Data use index (dataindex) where DataName="%s"'%gene)
    temp=c.fetchall()[0]
    dataid=temp
    c.execute('select DAValue from DAttribute use index (daindex_id) where DataID="%s" and DATypeID=1'%dataid)
    temp=c.fetchall()[0]
    gs=temp
    c.execute('select DAValue from DAttribute use index (daindex_id) where DataID="%s" and DATypeID=10'%dataid)
    temp=c.fetchall()[0]
    geneid=temp
    c.execute(('select DAValue from DAttribute use index (daindex_id) where DataID="%s" and DATypeID=3'%dataid))
    temp=c.fetchall()[0]
    bp=temp
    c.execute(('select DAValue from DAttribute use index (daindex_id) where DataID="%s" and DATypeID=4'%dataid))
    temp=c.fetchall()[0]
    cc=temp
    c.execute(('select DAValue from DAttribute use index (daindex_id) where DataID="%s" and DATypeID=5'%dataid))
    temp=c.fetchall()[0]
    mf=temp
    db.commit()
    print 'Content-type: text/html'
    print
    print '<html><head>'
    print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
    print '</head>'
    print '<body>'
    print '<h2>Gene Information</h2>'
    print '<table>'
    print '<tbody>'
    print '<tr>'
    print '<td><b>Probe ID:</b> %s</td>'%gene
    print '</tr>'
    print '<tr>'
    print '<td><b>Gene ID:</b> %s</td>'%geneid
    print '</tr>'
    print '<td><b>Gene Symbol:</b> %s</td>'%gs
    print '</tr>'
    print '<tr><td><b>GO Biological Process:</b></td></tr>'
    print '<tr><td>%s</td></tr>'%bp
    print '<tr><td><b>GO Cellular Component:</b></td></tr>'
    print '<tr><td>%s</td></tr>'%cc
    print '<tr><td><b>GO Molecular Function:</b></td></tr>'
    print '<tr><td>%s</td></tr>'%mf
    print '</tbody>'
    print '</table>'
    print '</body>'
    print '</html>'


if __name__=="__main__":
    main()
                    
                
