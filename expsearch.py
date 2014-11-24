#! /usr/bin/python
import os, cgi, MySQLdb

def main():
    form=cgi.FieldStorage()
    exp=form.getfirst('expname')
    db=MySQLdb.connect(host="localhost",user="root",passwd="")
    c=db.cursor()
    c.execute('use athaliana')
    c.execute('select DataID from Data use index (dataindex) where DataName="%s"'%exp)
    temp=c.fetchall()[0]
    expid=temp
    c.execute('select DAValue from DAttribute use index (daindex_id) where DataID="%s" and DATypeID=6'%expid)
    temp=c.fetchall()[0]
    gb=temp
    c.execute('select DAValue from DAttribute use index (daindex_id) where DataID="%s" and DATypeID=7'%expid)
    temp=c.fetchall()[0]
    tissue=temp
    c.execute(('select DAValue from DAttribute use index (daindex_id) where DataID="%s" and DATypeID=9'%expid))
    temp=c.fetchall()[0]
    treatment=temp
    db.commit()
    print 'Content-type: text/html'
    print
    print '<html><head>'
    print '<title>Arabdopsis Athaliana Microarray Data Browser</title>'
    print '</head>'
    print '<body>'
    print '<h2>Experiment Information</h2>'
    print '<table>'
    print '<tbody>'
    print '<tr>'
    print '<td><b>Experiment ID:</b> %s</td>'%exp
    print '</tr>'
    print '<tr>'
    print '<td><b>Genetic Background:</b> %s</td>'%gb
    print '</tr>'
    print '<tr><td><b>Tissue:</b> %s</td></tr>'%tissue
    print '<tr><td><b>Treatment:</b></td></tr>'
    print '<tr><td>%s</td></tr>'%treatment
    print '</tbody>'
    print '</table>'
    print '</body>'
    print '</html>'


if __name__=="__main__":
    main()
                    
                
