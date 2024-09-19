import asyncio
from ollama import AsyncClient
sys = """介绍啊，
那我下面就直接进入主题，
就讲我今天的内容就是我们居身智能的这样的一个 PI 模型感知想象和执行。
呃，
因为那我前面的一些就呃当然说这个愿景当然来自于今天来这里的肯定关起楚，
就是我们的愿景的时候，
实现通用机器人啊，
我比较喜欢这部电影呢，
是因为这部电影觉得是我认为在可见的未来是我们所有的东西都能够实现的啊，
但西部世界可能比较遥远啊，
这部电影我觉得是可能实现的。
大家有兴趣可以看一谈啊。
当然据身智能的话呃，
我就不多讲了，
这个啊在很早的图灵时代已经就提出了这样的一个居身智能的概念。
为什么它学术上是一个嗯从智能是一个更加是一个智能，
是一个啊非常高的一个智能的水平，
是因为它是因有身体跟身体联合去学习。
就像我们这个，
当然这个实验这个个人讲了很多呢，
我觉得快速讲一下，
就是呃那认知学的实验室，
它有两只的，
然后这只猫是主动来走另一只猫，
它出身就把它关起来，
但是他看的东西是一样的。
那最后这只猫把它被动的猫它下来之后，
它就失去了行为能力啊，
那这是为什么呢？
这是因为啊这个这个这个它没有居于身体的智能，
所以说他就失去了这种行为的能力。
好，
这也是证明了居人智能的重要性。
当然到今天我就不用讲那么多不言而喻啊。
因为我记得我我之前的讲座还得讲一堆什么是居生智能，
可能就就快速跳过了。
好，
那么我们的我们是当然说现在居人智能肯定是大家要做很多种技术路线嘛，
对吧？
啊，
那么我们也一直在探索我们一六的开始探索一种啊什么样的一个技术智能情框架，
就是它学术的底座应该什么样子。
那我们就类比人的模块，
我们把三这个部分就是大居身感知，
居然想象居人执行啊，
这是什么逻辑呢？
就是其实我们做件事情的话，
我们首先要知道它这个感知到这个世界的模型。
然后的话其实脑子里是在想象的，
就是我们做一件事情，
脑子是在动脑的。
比如说我要把它拧开，
我脑子是是过了一遍了，
只是那个我们自己下意识没感觉而已。
这属于是大脑功能，
我们把这个世界抽象出来。
然后第二部分就是执行执行是完全小脑的功能。
大家觉得哎，
那执行是不是比较简单，
我想完就能做，
其实并不是那么简单的。
因为它涉及到我们其实身体和下意识反应啊，
这个我会后面会专门展开讲，
所以说就是这两部分对于世界这个功能是对于大脑对世界理解和抽象，
最后我们要具象的去执行。
那我们就展开讲。
那第一个部分就是那个具身的感知了。
当然说大家可能看过很多大家都做机缘式，
如果做机缘视觉知道的感知，
但是我们需要的感知有什么不一样呢？
呃，
其实这里面有一个科学问题，
就是说如何去通用的去估计物理的常识啊，
那这件事情我们觉得都很容易是吧？
哎，
但其实不这么容易，
就是我们把这个箱把这个把这个盒子给它检测出来，
是比较容易的。
但是你要推断出这里是可以操作，
这个轴可以翻开，
这是有有难度的。
那么这件事情呢，
而我们就通用的做到我们专门去训练，
可能就意思不不是很有意思了。
那么这个事情呢，
其实在呃二二年时候一篇 nature behavior 的文章也就讲了深度学习这件事情，
其实现在是做不到的比较乏力。
那么去仔细想它的这个问题是怎样的呢？
啊，
然后呢我们觉得那在大模型今天非常强大的。
当天今天其实很多时候是卡在数据上面的。
那么这里面就是如何大规模的获得这种带有带有这种操作常识的数据是件很难的事情。
就比如上面我们知道这是可以翻开是可以拉的这是一件很难的事情啊，
那么我们就去创一个什么思路呢？
这个思路就是说我我们能推了这样的一个问题。
就是说哎我们发现原来这个手的操作和这个这个物体的操作常识，
它存在一种对偶关系啊，
我们验证了说哎，
我们们通过手操操作，
我们就能推这样样一一个一个物体怎么怎么样的一个一种操作作识，
而操作知识我们就能够够去生生成个手手操操作这种偶偶关系。
那么发现种对偶关系呢有什么好处？
首先这是可以是是最自然的数据，
而且是准确的可以被规模化的啊。
那这就是说呃比起你在那个三 d 里面去标，
它是更加准确的对规模化的。
那么为此的话呢，
我们就去构建了那个一系列的算法去去推断这些事情啊，
因为时间有限，
我就不讲了啊，
这个总之这样我们就将怎么去做手部重建以及手的在里面提取物体的知识啊，
这是一些提取出来的一些操作知识的结果。
啊，
那么那么我们这里因此还构建了一个一系列的一个系统。
啊，
这个系统的话是说怎么样快速的去通过手的操作啊，
上面是视频，
下面是对视频的解析，
下面是对手的一个分析。
手的分析。
我们能够去知道哎它在做一个什么概念，
这个物体应该是被怎么操作的。
那用这种方法我们快速能制备海量的数据。
那有这样数据的话呢，
我们发现这个模型的准确率是会被大大的提升啊，
也为这样的通用的将来做一个通用的这样的一个世界模型。
有个困角的 order model。
就是说我们看到什么事情们知道怎么去操作它啊，
这样的事情带来一个非常好的基础。
当然说基将的大数据之后呢，
我们就是会去啊去训练这样的一个物体的知识的模型。
就比如说像这些啊，
这本呢也得到了一个很大的提高啊。
好，
因为时间有限，
我跳到下一部分。
其实大家还可能想到，
那哎柔性物体怎么办？
对吧？
我体比是简单柔性物体的话，
其实我们也可以用这种方法。
但是我们是在 VRAR 眼镜里面，
然后呢我们配合上仿真引形，
比如叠衣服这样的叠的过程中，
其实我们是操作这个叠的知识被记录下来。
当然这里面还有一个环节是我们衣服操作，
完了我们要跟真机进行仿真对齐。
就是我们是这种是在仿真里面训的，
当然是是用手的操作记录它的操作知识。
最后的我们要跟真机对齐，
可能需要这么一步啊，
这是唯一不一样的。
那么为此的话，
我们就能够做到了。
应该我认为是第一个实际上第一个能够去做任意啊物体的物物体的那个呃衣服的操作。
因为衣服它的难点是跟比如去抓个东西啊，
或拉的东西不一样，
它是它整个状态是不确定的。
而且你看刚才我们扔进去的衣服是状态不确定的。
呃，
那么相比于呃像之前的方法的话，
他们是首先衣服要铺的比较好，
而且它叠的它是一个纯色的啊，
它要叠起来的话，
需要很多的很很很的那个就是相对来说是比较简单的，
我们是能做复杂的。
那么我们有了这样的一个知识之后呢，
我们可以干什么事情呢？
我们可以做交互感知了。
比如说我们现在从从能感知到这个微波炉啊，
是可以这样拉的啊。
但是说我们感知到微波炉之后，
我们发现还是有问题呢啊，
就是它感知可能不准，
那我们就引入了交互去纠正它的感知啊，
那么怎么做呢？
因为我们去拉的时候呢，
我们能够预判它下一步应该怎么样子。
因为我们有这个世界的模型，
对吧？
我们可以估计，
那么我们就可以真实的对比。
像这个是我们估计的，
是我们真实的。
然后我们去最小化它的误差，
哎，
最小化它误差就会逼着什么逼这个模型必须估计对你估计不对的话，
你这个你这个事情就就会出错。
那通过这个 loss 之后呢，
我们就可以看到这个这个序的事情，
就是我们从开始这个世界的模型有一点点的错误。
通过操作过程中呢，
引入这个操作者的纠正，
然后我们就能够把这个这个误差呃大量的大大量的大量的下正。
然后呢，
在此的话呢，
我们有另一个工作作，
我们可以把把这个东西放到呃更难的。
比如穿针上面，
而且我们这个东西不只是对于这个真的模型，
而且我们会带上那个观测的机械臂啊，
这个观测机械臂的话啊，
可以去看到说去地形不停的对它的纠正，
这也是获得今年的呃国际机器人体会 IS 的最佳系统论文提名啊是唯一的法原单位。
好，
下面我们就有了感知到基本知道这个世界什么样子，
那我们脑子肯定要过一遍了。
那为什么这件事情那么重要的？
因为我们脑子里的话，
仿真是把这种物理的约束加进去的。
所以说我们就会一个科学问题是如何把物理知识的约束啊，
去降低开发环境下的那个决策学习。
啊，
那么这个机器人的话呢，
这是一个全新的问题啊，
为什么呢？
因为它要求又准又快啊，
这是很复杂的问题啊。
当然仿真引擎大家可能知道的多了，
有游戏仿真引擎啊，
它快，
但物理上不准工业引擎，
它准，
但是它不够快。
因为我们机器学习是需要机械学习，
要高速的和那个仿真引擎进行交互。
对，
因此的话呢，
因此的话呢我们就呃因此我们的话我们就是对这个数学物理方程进行了重写，
以及做了很多软件工程的工作。
之前他们有求快呢，
他们是为了是要把各个模态进行独立的，
而我们建立了联合方程，
还有很多呃细节我就不讲了。
包括你看，
如果他们不这么做，
他们的穿模，
而我们就能够非常好的在这种多态中能够取得非常好的那个仿真效果。
我们的实验也表明了我们的速度能提升四百多倍，
跟最好的工业软件。
我们的误差在一毫米内，
就是能够支持高水平的物理仿真和同时能够呃同时能够呃同时能够快速的响应这样的一个机器人仿真系统啊，
机器人的那个真机系统。
啊，
这时候你会看到是我们呃我们跟力学，
这是我们的那个用用仿真的这是真机的力学。
我们测出来的这个误差是相对比较小的，
也是在里面有很多数学物理万物理方程来在在支撑。
所以我们对柔性物体的仿真呃在底层上去重写了它的那个数学物理方程，
还有像那个输液啊等等，
还有那个水流啊，
这些都是一些呃非常有难度的这些呃仿真啊，
但是关键它速度要快好啊，
这是还有它的渗透系统啊，
就相当于是这是把物理的那种规律嵌到这个学习系统里面，
导致它的准确率会更高。
呃，
那好，
那我们是相比于国际上的这几个仿真引擎，
包括 stanford，
还有那个 MIT 啊，
我们有以下的优势。
从公开发表的结果看啊，
有以下和啊这种是开源的啊，
就是 logo flow。
大家可以搜一下啊，
已经有康奈尔的之类，
呃，
多个单位在使用发了论文。
好，
那么有了这个事情的话，
我们能干些什么？
很有趣的事情呢？
我们一个非常好的一个物理仿真是必须快跟人工智能系统那个高速的一起。
对，
并撞的话，
我们通过深速学习规划之后呢，
我们就会得到一个真实场景。
那么脑子里其实有一个仿真引擎，
对吧？
我们仿真这个物理参数，
但这物理参数我们不可能去测量的那我我们可以仿仿它的的物理参数。
如果你仿真错了，
你真真实情况是一个误差的。
我们通约这个误差逼逼着它这个物参参必须得对，
才能够跟真机跟真实场景一致，
那就逼着它去估计这个真实的物理参数，
像这个叠衣服，
包括这么多量啊，
我们就是等于说整个系统的高速的跑起来，
仿真和深度学习能联合的跑起来。
哎，
那么我们就可以看到说，
哎，
下面是真机，
下面是仿真这种柔性物体，
其实钢体还比较好弄，
柔性物体是非常难的。
我们能够不能说分毫不差，
那是很接近，
导致我们的行为能比较准确啊，
那么这是我们估计出来的各种的那个物理参数和真实的比较还是很接近的。
啊。
好呃，
那么当然说这个事情的话，
那当然我们进一步有这仿真引擎，
同时可能也会支持这个海量的视频去学习那个实践的行为啊，
去实现那个行为。
啊，
当然说为此我们还构建了从怎么样从那个演示视频和仿真系统对齐的这个一个系统啊，
然后最后切入到真机。
因为时间有限，
我这就啊不讲了，
这也获得了 i loss 的呃 ISS 的，
不是那个按那个 i loss 的最佳论 m 机啊，
这是我们的整个拍拍断视频，
理解对接到仿真。
然后最后到真机，
把刚才那整套把它串起来。
好，
那么最后是居身执行。
呃，
这个事情其实是一个大家可能没感觉到，
让我们觉得很疼的一个问题。
就你看现在来说，
为什么我们觉得大脑规划完就结束呢？
其实不是我们实现下来是我们人为什么觉得大脑就结搞完就结束，
是因为我们一个神经下意识反应，
就是我们一个大小脑和这个神经系统，
使得我们呃神经系统使得我们那个能够去去下意识，
去做很多东西。
但是机器人如何去实现这种鲁棒的下意识呢是很关键的。
因为机器人存在感知误差、
仿真误差，
还有机械误差，
其实人也是一样的。
其实大家有没有觉得我们的感知其实是有误差的。
就是比如说我们去感知个东西，
我们脑子里其实这么想，
但其实我们闭上眼睛的时候，
其实很大的误差。
嗯，
那么这个时候呢就是这个误差怎么样？
人工智能把它吃掉。
呃，
这也就是说为什么能吃掉？
是因为我们刚才有个规划，
其其规划里里有底层层实有一个又一睛的那个子的那个原子的那个操作。
如果那个原子操作能够能够被通用化，
被这个人工智能吃掉的话，
哎，
那么我们就有可能去做成这样的一个事情啊，
那么这为什么能做到呢？
是因为其实它和同一个动作，
它其实在拓扑上同源的，
比如这个翻的动作其实之后会拓扑同源到这个东西，
这个不轴转这个事情，
所以有存在一种可能性。
嗯，
那么为此我们会去解决这样的一个操作的问题。
我们第一步是要解决通用的抓取问题。
那么通用的抓取问题，
它的最大的问题是数据困境还是回到的数据问题。
就是说哎我们有这么多的点云，
那我们怎么会变成怎么变成这些抓取的密集数据之前是没办法去制备这种大规模的数据的。
呃，
因此呢我们提出了一套啊半自动的那个数据的那个采集方式，
我们的整个的数据效率提高了标注，
提高了一万倍。
啊，
那使得我们能够快速的大规模的制备啊，
大量的那个数据，
不然的话很长时间啊，
基本原理是啊，
我们通过那个这是真实点云，
然后我们有一套数字完成系统，
能够去通过这枚数字完成到这里，
然后我们可以生成它的呃抓取的，
在用用仿真生成它抓取取点云，
然后就可以在真实的点云上打上很多标签，
大然在整套系统是里面嵌了很多算法和半自动的这样的系统。
啊，
为此我们能够大大的扩展了，
是比目前数集啊是二十一个数据，
有效数据能够有效的扩张到啊十万倍这样的数据，
而且标注的效率会大大提高。
那么也配套提出了新的那个大模型的那个抓取大模型的算法啊，
这里就不展开来讲。
那么呃为此的话呢呃我们就会因此我们得到了一个通用的抓取的模型。
那么通用抓取模型，
我们跟别的抓取有的不一样，
我们没见过的时候，
我们都能够去抓。
比如我们刚才这个东西被敲碎，
这个瓷器被敲碎瞬间其实每一个快都是没有见过的，
但没有见过。
我们仍然能够把它抓起来啊，
我们是在五千个呃没有见过，
完全没有见过的物体上面能够能够被被被通用的抓取。
包括我们也扩张到了那个去动态的物体。
这也是世界上第一个能够抓通用的，
没有抓，
没有通过见过的那个物体的抓鱼，
就呃抓那个没有见过的动态的物体啊，
这个也发表在那个机器人的底盘。
TIO 上面啊，
我们也是首次去呃跟人类比较超过人类水平，
通准确率和速度上面。
所以没有见过物物的的抓取，
超过人类水平，
也被斯坦福的那个机器人抓取排行榜，
被被被那个评为近十年影响力第二名。
好，
那么最后讲的一个就是以秘诀为中心的框架。
呃，
我们会思考一个问题，
就是说哎那么我们的话就是说我们之前谷歌不是提出了一种大模型嘛，
我们我在反思一下我们的大模型啊，
就是它是视觉输入，
然后通过大模型去得到一个位置决策。
哎，
那这种事情有什么问题呢？
看起来是没问题的，
但是你会没有发觉，
他们就这个更多的做移动，
把这个东西移到了另一个地方，
就是没有做那种 rich contact，
是那个那个 rich context 侧，
是那种呃那个很丰富的接触。
而这个事情呢，
我们如果需要突破很复杂的接触的问题，
那我们需要以立觉为中心的一个框出，
就是位置引导下的率反馈的一个输出。
那么因此构建了这样的立觉的一个事情，
去去做这样的一个事情。
那我们来看看有一件事情，
就是位置控制的一定是做不了的。
就我们光这个气球啊，
你你你想这个问题，
如果我们要位置控制，
你只要往下错一毫米就爆掉了，
网上上一毫米就刮不干净。
所以这里面它的我们这个模型的输出是用大模型输出的，
它的力的摁压力是多少，
以及它倾向力是多少。
但是可能大概有个位置的一个引导。
所以如果未来用到的家用医疗等数和这个一个非常好的力反馈的一个力觉大模型来做这样的一个事情。
这也是我们一直在呃希望在做这样的一个在在做的一个过程。
那包括我们的能够做到非常精密的那种这种力的控制就是轮扩到它这样。
那其实也是说会在你的力觉参数和这个位置引导是由模型来输出。
这就是说以力觉为中心会是将来去解决这个小脑这部分很关键的一个一个点。
啊，
为此的话我们也是开源了线上的最大的。
目前最大的以力觉为中心的数据集啊啊，
大家欢迎下载我们的数据集量是那个 GTP 数数据量的两倍。
我们拥有力觉、
听觉、
语言、
控制等觉等等这些这样的一个事情。
那我们的力的操作平台是比较特殊的。
我们能够哎 osorry 哦，
好，
这里其实是一张一个视频。
这本来是我们的切火机，
就是我们人去摇操作切火机，
能够去记录大量的那种底层的这种呃力反馈的数据。
然后当时我们位置位置为中心的模仿学习数据库，
我们也参与了啊，
我们是那个大概有四十个学校啊，
然后我们也是唯一的国内单位参与了那个对大规模的一个就呃 open x 一 body 的。
但是是基于那个位置仿真的啊一个呃位置，
基于位置规划的这样的一个数据啊，
也欢迎大家来使用。
好。
那么就是呃我们这是我们的综合的系统的结果。
嗯，
呃，
这是我们综合的系统的结果。
就是说 expert 呃呃就是就是我们我们把我们整体的各种技术整合进去，
做了一套呃综合的一个机器人，
呃，
比如做早餐啊清洁。
那你看这个擦东西，
其实我们为什么要擦东西？
因为擦东西要力卷，
因为力卷你擦不干净，
所以我们需要那个力的那个模型，
包括我们要去把壶拿进去啊，
这里面会整合到我们的柔性物体。
如果没有很好的，
刚才我们讲的钢铁还是比较容易。
当你柔性物体知道哪个是衣领的时候，
它的难度就会大大的增加。
好啊，
这是这是。
当然我们也把我们的很多的技术开源到我们的 mobl flow 啊，
我们一个上面有生态 tutorial document，
还有论坛还 github 等等连接能连接十四种机器人啊，
也希望大家以够啊多多支持我们啊，
当然最后我们时间有限来讲，
我们跟怎么去研究大脑和身体间的关系，
这是基因智能和一个行为上的一个很关键的一个事情。
然后时间到了。
哦，
好，
那那刚刚好呃，
那最后是我们这些呃做的一些论文，
就包括那个我们主要还在呃，
就就除了人工智能都还有机器人的两大顶刊上面还有获得的一些呃最佳呃，
各个会议的最机器人顶会最佳论文。
好，
我可能怕时间不够赶的太快啊。
最后呢讲一句就是呃感慨一下，
就是啊通用机器人是人工智能的终极状态。
我们认为积分智能是个灵魂，
也就是很有趣的一个领域啊，
希望大家能够也能够一起来来做这么一件啊，
让让人类更加美好的事情啊，
然后再次推荐大家看这部电影，
就是我每次在看的时候觉得哎你的动作我们怎么把它做成，
也是我们可以做成的范围内啊，
谢谢大家。
"""
from ollama import Client
def chat():
  message = {'role': 'user', 'content': sys}
  for part in  Client().chat(model='qwen2:72b-instruct', messages=[message],options= {
            "num_ctx": 30000 ,
            'num_predict' : 300
        }, stream=True):
    print(part['message']['content'], end='', flush=True)

chat()