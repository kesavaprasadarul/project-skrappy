import skrappy_01
import sys_core
import net_core

user = skrappy_01.LoginAsAdmin()
skrappy_01.AddItemToQueue(user,"https://amazon.in/dp/95123",95123,142, 95)
print(skrappy_01.GetCurrentQueue(user))