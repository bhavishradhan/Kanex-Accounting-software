import mysql.connector as mc
import datetime
from tkinter import *

todate=datetime.datetime.today()
today=str(todate.year)+'-'+str(todate.month)+'-'+str(todate.day)
mydb=mc.connect(host='localhost',user='root',passwd='root',database='tuckshop')
cur=mydb.cursor()
cur.execute("SELECT COUNT(ITCODE)+1 FROM ITEMS")
itcount=cur.fetchall()
itemcount=int(itcount[0][0])
cur.execute("SELECT ITCODE,TYPE FROM ITEMS")
z=cur.fetchall()
itlist=list(i[1] for i in z)


class storows():
    cur.execute("SELECT * FROM STORE")
    ro=cur.fetchall()
    row=cur.rowcount

    
class itrows():
    cur.execute("SELECT * FROM ITEMS")
    ro=cur.fetchall()
    row=cur.rowcount

    
def stockleft(item):
    subquery="SELECT STOCK_LEFT FROM ITEMS WHERE TYPE='{}'".format(item)
    cur.execute(subquery)
    stoc=cur.fetchall()
    stoc=int(stoc[0][0])
    return stoc
def instore(item,no,qty,tot):
    global today,itlist
    stock=stockleft(item)
    query="INSERT INTO STORE VALUES({},'{}',{},{},'{}')".format(no,itlist.index(item)+1,qty,tot,today)
    cur.execute(query)
    mydb.commit()
    query4="UPDATE ITEMS SET STOCK_LEFT={} WHERE ITCODE='{}'".format(stock-1,itlist.index(item)+1)
    cur.execute(query4)
    mydb.commit()

    
def pritems(t):
    stmt="SELECT PRICE FROM ITEMS WHERE TYPE='{}'".format(t)
    cur.execute(stmt)
    typ=cur.fetchall()
    x1=float(typ[0][0])
    return x1
def amount(price,item):
    query1="UPDATE ITEMS SET PRICE={} WHERE TYPE='{}'".format(price,item)
    cur.execute(query1)
    mydb.commit()

    
def new(itlist,item,price,stock):
    query2="INSERT INTO ITEMS VALUES('{}','{}',{},{})".format(len(itlist)+1,item,price,stock)
    try:
        cur.execute(query2)
        mydb.commit()
        print('RECORD INSERTION SUCCESSFUL')
    except Exception as e:
        print(e)
    except mysql.connector.Error() as er:
        print(er)

        
def add(qty,item):
    query3="UPDATE ITEMS SET STOCK_LEFT={} WHERE TYPE='{}'".format(qty,item)
    cur.execute(query3)
    mydb.commit()

    
def delete(item):
    query5="DELETE FROM ITEMS WHERE TYPE='{}'".format(item)
    cur.execute(query5)
    mydb.commit()

    
def clear_mod(a,b,c,f):
    a.delete(0,END)
    c.delete(0,END)
    b.delete(0,END)
    f.focus_set()

    
def clear_bill(a,b,f):
    a.delete(0,END)
    b.delete(0,END)
    f.focus_set()

    
def clear():
    clear_bill(itemch5,stocklft,itemch5)

    
def modwin():
    root1=Tk()
    root1.geometry("400x400")
    root1.configure(bg='skyblue')
    root1.title("MODIFY")
    
    def newwin():
        root4=Tk()
        root4.title("NEW")
        root4.geometry("300x230")
        root4.configure(bg='skyblue')
        Label(root4,text="ENTER NEW\nITEM NAME:",font='georgia',bg='skyblue').grid(row=1,column=0)
        Label(root4,text="ENTER QTY:",font='georgia',bg='skyblue').grid()
        Label(root4,text="ENTER PRICE:",font='georgia',bg='skyblue').grid()
        itemqty=Entry(root4)
        itemch1=Entry(root4)
        itemprice=Entry(root4)
        itemch1.grid(row=1,column=1,ipady=5,pady=4)
        itemqty.grid(row=2,column=1,ipady=5,pady=4)
        itemprice.grid(row=3,column=1,ipady=5,pady=4)
        
        def get_new():
            global newit,newqty,newprice,itlist
            newit=itemch1.get().upper()
            newqty=itemqty.get()
            newprice=itemprice.get()
            new(itlist,newit,newprice,newqty)
            clear_mod(a=itemch1,b=itemqty,c=itemprice,f=itemch1)
        submit1=Button(root4,text="SUBMIT",font='georgia',command=get_new)
        submit1.grid(row=4,column=1,ipadx=5,pady=4)
        backb=Button(root4,text="BACK",fg='red',font='elephant',command=root4.destroy)
        backb.grid(row=5,column=1,pady=4)
#-----------------------------------------------------------------------------#
    def addwin():
        root5=Tk()
        root5.title("ADD")
        root5.geometry("300x200")
        root5.configure(bg='skyblue')
        Label(root5,text="ENTER ITEM NAME:",font='georgia',bg='skyblue').grid(row=1,column=0)
        Label(root5,text="ENTER QTY TO\nBE ADDED:",font='georgia',bg='skyblue').grid(row=2,column=0)
        itemch2=Entry(root5)
        itemqty2=Entry(root5)
        itemch2.grid(row=1,column=1,ipady=5,pady=4)
        itemqty2.grid(row=2,column=1,ipady=5,pady=4)
        
        def get_add():
            global addit,adqty
            addit=itemch2.get().upper()
            adqty=itemqty2.get()
            adit=stockleft(addit)+int(adqty)
            add(adqty,adit)
            clear_bill(a=itemch2,b=itemqty2,f=itemch2)
        submit2=Button(root5,text="SUBMIT",font='georgia',command=get_add)
        submit2.grid(row=3,column=1,ipadx=5,pady=4)
        backb2=Button(root5,text="BACK",fg='red',font='elephant',command=root5.destroy)
        backb2.grid(row=4,column=1,pady=4)
        
#-------------------------------------------------------------------------------#
    def remwin():
        root6=Tk()
        root6.title("REMOVE")
        root6.geometry("310x200")
        root6.configure(bg='skyblue')
        Label(root6,text="ENTER ITEM NAME:",font='georgia',bg='skyblue').grid(row=1,column=0)
        Label(root6,text="ENTER QTY TO\nBE REMOVED:",font='georgia',bg='skyblue').grid(row=3,column=0)
        itemch3=Entry(root6)
        itemqty3=Entry(root6)
        itemch3.grid(row=1,column=1,ipady=5,pady=4)
        itemqty3.grid(row=3,column=1,ipady=5,pady=4)
        
        def get_rem():
            global remit,remqty,remitem
            remitem=itemch3.get().upper()
            remqty=int(itemqty3.get())
            remit=stockleft(remitem)-remqty
            add(remit,remitem)
            clear_bill(a=itemch3,b=itemqty3,f=itemch3)
            
        def rem():
            remitem=itemch3.get().upper()
            rem=delete(remitem)
            clear_bill(a=itemch3,b=itemqty3,f=itemch3)
        fullrem=Button(root6,text="REMOVE FULLY",font='georgia 12 italic',command=rem)
        fullrem.grid(row=2,column=1)
        submit3=Button(root6,text="SUBMIT",font='georgia',command=get_rem)
        submit3.grid(row=4,column=1,ipadx=5,pady=4)
        backb3=Button(root6,text="BACK",fg='red',font='elephant',command=root6.destroy)
        backb3.grid(row=5,column=1,pady=4)
#---------------------------------------------------------------------------------#
    def prcwin():
        global itemprc
        root7=Tk()
        root7.title("PRICE")
        root7.geometry("300x200")
        root7.configure(bg='skyblue')
        Label(root7,text="ENTER ITEM NAME:",font='georgia',bg='skyblue').grid(row=1,column=0)
        Label(root7,text="ENTER NEW PRICE:",font='georgia',bg='skyblue').grid(row=2,column=0)
        itemch4=Entry(root7)
        itemprc=Entry(root7)
        itemch4.grid(row=1,column=1,ipady=5,pady=4)
        itemprc.grid(row=2,column=1,ipady=5,pady=4)

        
        def get_prc(event=None):
            global itprc,prcitem
            itprc=itemch4.get().upper()
            prcitem=itemprc.get()
            amount(prcitem,itprc)
            clear_bill(itemch4,itemprc,f=itemch4)
        submit4=Button(root7,text="SUBMIT",font='georgia',command=get_prc)
        root7.bind("<Return>",get_prc)
        backb4=Button(root7,text="BACK",fg='red',font='elephant',command=root7.destroy)
        submit4.grid(row=3,column=1,ipadx=5,pady=4)
        backb4.grid(row=4,column=1,ipadx=5,pady=4)
#--------------------------------------------------------------------------------#
    def stockwin():
        global itemch5,stocklft
        root8=Tk()

        root8.title("STOCK LEFT")
        root8.geometry("300x200")
        root8.configure(bg='skyblue')
        Label(root8,text="ENTER ITEM NAME:",font='georgia',bg='skyblue').grid(row=1,column=0)
        Label(root8,text="STOCK LEFT  =",font='georgia',bg='skyblue').grid(row=2,column=0)
        itemch5=Entry(root8)
        stocklft=Entry(root8)
        itemch5.grid(row=1,column=1,ipady=5,pady=4)
        stocklft.grid(row=2,column=1,ipady=5,pady=4)

        
        def get_stock(event=None):
            global itstock,fullstock
            itstoc=itemch5.get().upper()
            stocklft.insert(0,stockleft(itstoc))

            
        def full():
            root9=Tk()
            root9.title("FULL LIST")
            root9.geometry("200x200")
            root9.configure(bg='skyblue')
            Label(root9,text="LIST OF STOCK LEFT",bg='skyblue',fg='blue',font='forte').grid()
            for i in itlist:
                itst=i,":",stockleft(i)
                showst=Label(root9,text=itst,font='georgia',bg='skyblue',fg='maroon')
                showst.grid()
        root8.bind("<Return>",get_stock)
        fullist=Button(root8,text="FULL LIST",font='georgia',fg='blue',command=full)
        fullist.grid(row=5,column=0,ipadx=5,pady=4)
        submit5=Button(root8,text="SUBMIT",font='georgia',command=get_stock)
        submit5.grid(row=3,column=1,ipadx=5,pady=4)
        clearb=Button(root8,text="CLEAR",font='georgia',command=clear)
        clearb.grid(row=4,column=1,ipadx=5,pady=4)
        backb5=Button(root8,text="BACK",font='elephant',fg='red',command=root8.destroy)
        backb5.grid(row=5,column=1,ipadx=5,pady=4)
    newb=Button(root1,text="       NEW        ",font='georgia',fg='black',bg='silver',command=newwin)
    addb=Button(root1,text="       ADD         ",font='georgia',fg='black',bg='silver',command=addwin)
    removeb=Button(root1,text="    REMOVE   ",font='georgia',fg='black',bg='silver',command=remwin)
    priceb=Button(root1,text="       PRICE     ",font='georgia',fg='black',bg='silver',command=prcwin)
    stockb=Button(root1,text="STOCK LEFT",font='georgia',fg='black',bg='silver',command=stockwin)
    backb=Button(root1,text="BACK",font='elephant',fg='red',bg='silver',command=root1.destroy)
    newb.pack(ipadx=10,ipady=3,pady=4)
    addb.pack(ipadx=10,ipady=3,pady=4)
    removeb.pack(ipadx=10,ipady=3,pady=4)
    priceb.pack(ipadx=10,ipady=3,pady=4)
    stockb.pack(ipadx=10,ipady=3,pady=4)
    backb.pack(ipadx=30,ipady=3,pady=4)

    
def billwin():
    root2=Tk()
    root2.geometry("300x200")
    root2.configure(bg='skyblue')
    root2.title("BILLING")
    itemch=Entry(root2)
    itemqty=Entry(root2)
    labelqty=Label(root2,text="ENTER QTY:",bg='skyblue',font='georgia')
    labelitn=Label(root2,text="ENTER ITEMNAME:",bg='skyblue',font='georgia')
    itemqty.grid(row=2,column=1,pady=10,ipady=4)
    labelqty.grid(row=2,column=0)
    labelitn.grid(row=1,column=0)
    itemch.grid(row=1,column=1,pady=10,ipady=4)
    itemch.focus_set()

    
    def get_it():
        try:
            global itchoice,itqty,d
            d={}
            total=0
            itchoice=itemch.get().upper()
            itchlst=itchoice.split(',')
            itqty=itemqty.get()
            itqtlst=itqty.split(',')
            for i in itchlst:
                d[i]=itqtlst[itchlst.index(i)]
            for i in d:
                rup=pritems(i)
                tot=rup*int(d[i])
                total+=tot
            #rupee=pritems(itchoice)
            #total=pritems(itchoice)*int(itqty)
                cur.execute("SELECT MAX(SLNO) FROM STORE")
                storeno=cur.fetchall()[0][0]+1
                instore(i,storeno,d[i],tot)
            clear_bill(b=itemch,a=itemqty,f=itemch)
            root3=Tk()
            root3.geometry('200x80')
            root3.title("BILL")
            root3.configure(background='skyblue')
            bill=Label(root3,text="BILL AMOUNT = ",font='georgia',bg='skyblue')
            bilamt=Label(root3,text=total,font='elephant',bg='skyblue')
            bill.grid(row=1,column=2,ipady=5)
            bilamt.grid(row=1,column=3)
            okb=Button(root3,text="OK",fg='red',font='georgia',command=root3.destroy)
            okb.grid(row=3,column=2)
        except TypeError:
            print("NUMBER OF ITEMS AND QTY DOESN'T MATCH")
        except Exception as e:
            print(e)
    submit=Button(root2,text="SUBMIT",font='georgia',command=get_it)
    submit.grid(row=3,column=1,ipadx=10)
    back=Button(root2,text="BACK",command=root2.destroy,font='elephant',fg='red')
    back.grid(row=5,column=1,pady=10)

    
root=Tk()
root.geometry("250x300")
root.configure(background='skyblue')
root.title("TUCKSHOP")
bill=Button(root,text="BILLING",font='Georgia',fg='black',bg='silver',command=billwin)
mod=Button(root,text="MODIFY",font='Georgia',fg='black',bg='silver',command=modwin)
log=Button(root,text="LOGOUT",font='Elephant',fg='red',bg='silver',command=exit)


for i in itlist:
    thing=i,':',pritems(i)
    show=Label(root,text=thing,bg='skyblue',font='Georgia',fg='blue')
    show.pack(side=BOTTOM)
Label(root,text="THINGS AVAILABLE:",bg='skyblue',font='forte',fg='blue').pack(side=BOTTOM)
bill.pack(side=TOP,ipadx=10,ipady=3)
mod.pack(ipadx=10,ipady=3,pady=5)
log.pack()
