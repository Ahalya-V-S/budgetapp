class Category:
  def __init__(self,description):
    self.ledger=[]
    self.description=description
    self.__balance=0.0
  def __repr__(self):
    str_repr = self.description.center(30,"*")+"\n"
    for transaction in self.ledger:
      description = transaction["description"]
      if len(description) > 23:
        description = description[:23]
      str_repr += description.ljust(23)
      str_repr += f"{transaction['amount']:.2f}".rjust(7)+"\n"
    str_repr += f"Total: {self.get_balance()}"
    return str_repr
  def deposit(self,amount,description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.__balance+=amount
  def withdraw(self,amount,description=""):
    if self.check_funds(amount):
      self.ledger.append({"amount": -1*amount, "description": description})
      self.__balance-=amount
      return True
    else:return False
  def get_balance(self):
    return self.__balance
  def transfer(self, amount, category_instance):
    if self.check_funds(amount):
      self.withdraw(amount,f"Transfer to {category_instance.description}")
      category_instance.deposit(amount,f"Transfer from {self.description}")
      return True 
    else:
      return False		
  def check_funds(self,amount):
    if self.__balance>=amount:
      return True
    else:return False
def create_spend_chart(categories):
  def withdraw_amt(category):
    withdraw=0
    for list in category.ledger:
      if(list["amount"]<0):
        withdraw+=abs(list["amount"])
    return withdraw
  total_withdraw=sum(map(lambda c:withdraw_amt(c),categories))
  percents=[]
  names=[]
  for c in categories:
    withdraw=withdraw_amt(c)
    p=withdraw*100/total_withdraw
    percents.append(p)
    name = c.description
    names.append(name)
  bar_chart = "Percentage spent by category\n"
  for i in range(100, -10, -10):
    line = f"{i}| ".rjust(5, " ")
    for percent in percents:
      if i <= percent:
        line += "o  "
      else:line += "   "
    bar_chart += line + "\n"
	
  bar_chart += "    -" + "-"*len(categories)*3 + "\n"

  max_len = max(map(lambda name: len(name), names))
  for i in range(len(names)):
    names[i]=names[i].ljust(max_len)
  for i in range(max_len):
    line="     "
    for name in names:
      line+=name[i]+"  "
    bar_chart += line + "\n"
  bar_chart = bar_chart.rstrip("\n")
  return bar_chart