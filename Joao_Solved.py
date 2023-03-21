class Category:
    
    def __init__(self, nam):
        self.name = nam
        self.ledger=[]
        self.balance=[]
    
    def deposit(self,amt,desc=""):
        self.ledger.append({"amount": amt, "description": desc})
        
    def withdraw(self,amt,desc=""):
        if self.check_funds(amt) == False:
            return False
        else:            
            self.ledger.append({"amount": -amt, "description": desc})
            return True
    
    def get_balance(self):
        self.balance=[i["amount"] for i in self.ledger]
        return sum(self.balance)
    
    def check_funds(self,amt):
        self.balance=[i["amount"] for i in self.ledger]
        if amt>sum(self.balance):
            return False
        else:
            return True
    
    def transfer(self,amt,cat):
        if self.check_funds(amt) == False:
            return False
        else:
            cat.ledger.append({"amount": amt, "description": "Transfer from "+self.name})
            self.ledger.append({"amount": -amt, "description": "Transfer to "+cat.name})
            return True
    
    def __str__(self):
        x=(self.name.center(30,"*")+"\n")
        for i in self.ledger:
            desc=i["description"][:23]
            am="{:.2f}".format(i["amount"])[:7]
            y=desc+"@"+am
            y=y.replace("@"," "*(31-len(y)))
            x+=y+"\n"
        tot="Total: "+"{:.2f}".format(sum([i["amount"] for i in self.ledger]))
        x+=tot
        return x


def create_spend_chart(args):

    per="Percentage spent by category"
    ten="100|"
    nine=" 90|"
    eight=" 80|"
    sev=" 70|"
    six=" 60|"
    fiv=" 50|"
    four=" 40|"
    thr=" 30|"
    two=" 20|"
    one=" 10|"
    zero="  0|"
    line="    "+("---"*len(args))+"-"
    sums=[zero,one,two,thr,four,fiv,six,sev,eight,nine,ten]
    
    
    tot=[]
    for cat in args:
        for i in cat.ledger:
            if i["amount"]<0 and ("Transfer" not in i["description"]):
                tot.append(i["amount"])
    tot=sum(tot)
    pert=[]
    for cat in args:
        temp=[]
        for i in cat.ledger:
            if i["amount"]<0 and ("Transfer" not in i["description"]):
                temp.append(i["amount"])
                
        pert.append(int((sum(temp)/tot)*10//1))
    
    for i in pert:
        for j in range(i+1):
            sums[j]+=" o "
        for j in range(1,11-i):
            sums[-j]+="   "
    
    catnames=[]
    for cat in args:
        catnames.append(cat.name)
    lenght=len(max(catnames, key=lambda x:len(x)))
    for name in range(len(catnames)):
        catnames[name]=catnames[name].ljust(lenght)
    bottom=['  '.join(chars) for chars in zip(*catnames)]
    for i in range(len(bottom)):
        bottom[i]="     "+bottom[i]+"  "

        
    
    sums.reverse()
    for i in range(len(sums)):
        sums[i]+=" "
    sums.append(line)
    
    final=per
    for i in sums:
        final+="\n"+i
    for i in bottom:
        final+="\n"+i

    return final