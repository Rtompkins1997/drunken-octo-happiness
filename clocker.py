'''
Created on Apr 18, 2014

@author: vittorio
'''
import wx
import time
import datetime

buff = ''
volunteer = []
TIMER_ID = 1
TIMER_ID1 = 2
update = False
go = True

class gui(wx.Frame):
    def __init__(self, parent, title):
        super(gui, self).__init__(parent, title=title, size=(530, 800))
        self.pnl = wx.Panel(self)
        
        self.lc = wx.ListCtrl(self.pnl, -1, style=wx.LC_REPORT, size=(390,350), pos=(10,10))
        self.lc.InsertColumn(0, 'User')
        self.lc.InsertColumn(1, 'Time Spent')
        
        self.lc1 = wx.ListCtrl(self.pnl, -1, style=wx.LC_REPORT, size=(390,350), pos=(10,380))
        self.lc1.InsertColumn(0, 'User')
        self.lc1.InsertColumn(1, 'Time Spent')
        self.lc1.InsertColumn(2, 'Savings')
        
        self.new_user = wx.Button(self.pnl, label='New User', pos=(410,10))
        self.clock = wx.Button(self.pnl, label='Clock In / Out', pos=(410,40))
        self.clock.Bind(wx.EVT_BUTTON, self.go_)
        
        self.new_user.Bind(wx.EVT_BUTTON, self.newUser)
          
        self.timer = wx.Timer(self.pnl, TIMER_ID)
        self.timer.Start(1000)       
        wx.EVT_TIMER(self.pnl, TIMER_ID, self.statusUpdate)
        
        self.timer1 = wx.Timer(self.pnl, TIMER_ID1)
        self.timer1.Start(5000)
        wx.EVT_TIMER(self.pnl, 2, self.statusUpdate2)
        
        #06340
        self.Show()
      
    def AddToDatabase(self, uid, hours):
        
        t = datetime.date.today()
        tt = str(t).split('-')
        tt = tt[0] + '-' + tt[1]
        
        lines = tuple(open('data.db', 'r'))
        new_lines = []
        print str(uid) + '\t' + str(hours)

        for m in lines:
            if str(m).startswith(uid):
                l = long(long(hours) + long(str(str(m).split(';')[2]).strip()))
                print l
                new_lines.append(str(uid) + ';'  + str(m).split(';')[1] + ';' + str(l) + '\n')
            else:
                new_lines.append(m)
        
        print new_lines
        
        n_w = ''
        for nl in new_lines:
            n_w += str(nl)
        
        f = open('data.db', 'w')
        f.write(n_w)
        f.close()
        
        global update
        update = True
        
    def go_(self,event):
        dlg = wx.TextEntryDialog(None, 'Please Scan you card')
        dlg.ShowModal()
        cn = dlg.GetValue()
        
        update = True
        index = 0
                
        lines = [line.strip() for line in open('data.db')]
        print lines
        add = False
        for m in lines:
                    
            buff = str(cn).strip()
            m = str(str(m).split(';')[0]).strip()
                    
            if m == buff:
                print ':)'
                add = True
                break;
                
        if add:
                
            try:
                        
                for v in volenteers[::2]:
                    if v == buff:
                        update = False
                        break;
                    index += 2
                                
            except:
                pass
                    
            if update:
                volunteer.append(buff)
                volunteer.append(time.time())
            else:
                        
                self.AddToDatabase(volunteer[index], long(time.time() - volenteers[index + 1]))
                volunteer.remove(volunteer[index + 1])
                volunteer.remove(buff)
                
            print volunteer
            global go
        
        
    def newUser(self, event):
        
        global go
        go = False
        
        self.timer.Stop()
        self.timer1.Stop()
        
        dlg = wx.TextEntryDialog(None, 'Please Scan you card')
        dlg.ShowModal()
        cn = dlg.GetValue()
        
        dlg = wx.TextEntryDialog(None,'Please Enter First And Last Name')
        dlg.ShowModal()
        fl = dlg.GetValue()
        
        lines = tuple(open('data.db', 'r'))
        new_lines = ''
        
        for p in lines:
            new_lines += p
        
        new_lines += str(cn) + ';' + str(fl) + ';' + str('0') + '\n'
        
        f = open('data.db', 'w')
        f.write(new_lines)
        f.close()
        
        self.timer.Start()
        self.timer1.Start()
        
        go = True
        
        pass
        
    def statusUpdate2(self, event):
        
        global update
        
        if update:
        
            lines = [line.strip() for line in open('data.db')]
            
            self.lc1.ClearAll()
            self.lc1.InsertColumn(0, 'User')
            self.lc1.InsertColumn(1, 'Time Spent')
            self.lc1.InsertColumn(2, 'Savings')
            
            self.lc1.SetColumnWidth(0,115)
            self.lc1.SetColumnWidth(1,115)
            self.lc1.SetColumnWidth(2,115)
            
            for ll in lines:
                
                ll = str(ll).split(';')
                pos = self.lc1.InsertStringItem(0, ll[1])
                
                timet = 0
                timet = float(ll[2])
    
                timet = float(timet) / 60
                timet = float(timet) / 60
                timet = "{0:.6f}".format(float(timet))
                self.lc1.SetStringItem(pos, 1, str(timet) + " hours")
                self.lc1.SetStringItem(pos, 2, "???")
                
        update = False
        
    def statusUpdate(self, event):
        index = 0
           
        lines = [line.strip() for line in open('data.db')]
        
        self.lc.ClearAll()
        
        self.lc.InsertColumn(0, 'User')
        self.lc.InsertColumn(1, 'Time Spent')
        
        self.lc.SetColumnWidth(0,190)
        self.lc.SetColumnWidth(1,100)
        
        for v in volenteers[::2]:
            
            for l in lines:
                if str(l).startswith(v):
                    v = str(l).split(';')[1]
                    break;
            
            pos = self.lc.InsertStringItem(0, v)
            self.lc.SetStringItem(pos, 1, str(long(long(time.time())) - long(volenteers[index + 1])) + ' seconds' )
            index += 2

if __name__ == '__main__':
    
    app = wx.App()
    s = gui(None,title='Fiddleheads Volunteer Discouts')
    app.MainLoop()
