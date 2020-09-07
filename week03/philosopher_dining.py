import threading 
import random
import time
import queue
#利用列队来进行消息共享

"""
问题描述：
测试用例：

输入：n = 1 （1<=n<=60，n 表示每个哲学家需要进餐的次数。）
预期输出：

[[4,2,1],[4,1,1],[0,1,1],[2,2,1],[2,1,1],[2,0,3],[2,1,2],[2,2,2],[4,0,3],[4,1,2],[0,2,1],[4,2,2],[3,2,1],[3,1,1],[0,0,3],[0,1,2],[0,2,2],[1,2,1],[1,1,1],[3,0,3],[3,1,2],[3,2,2],[1,0,3],[1,1,2],[1,2,2]]
解释:

输出列表中的每一个子列表描述了某个哲学家的具体行为，它的格式如下：
output[i] = [a, b, c] (3 个整数)

a 哲学家编号。
b 指定叉子：{1 : 左边, 2 : 右边}.
c 指定行为：{1 : 拿起, 2 : 放下, 3 : 吃面}。
如 [4,2,1] 表示 4 号哲学家拿起了右边的叉子。所有自列表组合起来，就完整描述了“当每个哲学家分别需要进食 n 次”时这五位哲学家具体的行为记录。
"""

class DiningPhilosophers(threading.Thread):
    def __init__(self,philosopher,times,q,leftLock,rightLock):
        #conn条件锁，threadno线程个数，times吃面的次数
        super().__init__()
        self.philosopher=philosopher
        self.times=times
        self.q=q
        self.leftLock=leftLock
        self.rightLock=rightLock


    def run(self):
        #进入只要times大于0就一直循环
        while self.times>0:

            #每次循环开始时就进入思考
            self.think()

            #尝试拿左叉，等待一秒，如果拿不到则跳到下一次循环
            pickLeftFork=self.leftLock.acquire(timeout=1)
            if not pickLeftFork:
                continue
            else:
                self.pickLeftFork()

            pickRightFork=self.rightLock.acquire(timeout=1)
            if pickRightFork:
                #如果拿到右叉
                self.pickRightFork()
                self.eat()
                self.putLeftFork()
                self.putRightFork()
                self.times-=1
                print(f'哲学家{self.philosopher}结束用餐，还需就餐{self.times}次')
            else:
                self.putLeftFork()
                print(f'哲学家{self.philosopher}用餐失败，重新就餐')


    def think(self):
        print(f'哲学家{self.philosopher} 正在思考')
        time.sleep(random.randint(1,3))

    def pickLeftFork(self):
        print(f'哲学家{self.philosopher} 拿起左叉，准备拿起右叉')
        self.q.put([self.philosopher,1,1])

    def pickRightFork(self):
        print(f'哲学家{self.philosopher} 拿起右叉，准备用餐')
        self.q.put([self.philosopher,2,1])

    def eat(self):
        print(f'哲学家{self.philosopher} 正在用餐')
        self.q.put([self.philosopher,0,3])

    def putLeftFork(self):
        print(f'哲学家{self.philosopher} 放下左叉')
        self.q.put([self.philosopher,1,2])
        self.leftLock.release()

    def putRightFork(self):
        print(f'哲学家{self.philosopher} 放下右叉')
        self.q.put([self.philosopher,2,2])
        self.rightLock.release()

if __name__=='__main__':

    philosopher=list(range(5))#哲学家编号为0，1，2，3，4
    while True:
        try:
            times=int(input('请输入每个哲学家需要用餐的次数：'))
        except Exception as err:
            print(err)
        if (0<times) &(times<60):
            break
        
    
    q=queue.Queue()

    locks=[threading.Lock() for i in range(5)]

    t=[]

    for i in range(5):
        if i< 4:
            t.append(DiningPhilosophers(philosopher[i],times,q,locks[i],locks[i+1]))
        else:
            t.append(DiningPhilosophers(philosopher[i],times,q,locks[i],locks[0]))

    for i in t:
        i.start()

    for i in t:
        i.join()

    #打印记录
    records_list=[]
    while not q.empty():
        records_list.append(q.get())
    print(f'哲学家行为记录为:\n{records_list}')

