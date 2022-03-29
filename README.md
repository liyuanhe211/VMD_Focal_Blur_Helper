# VMD Focal Blur Helper
A program to help build accurate focal blur into a POV-Ray render file generated by VMD/

# Translation in process :hourglass_flowing_sand:

VMD中实现带焦点虚化的渲染颇为不便，结合Techyon实现时，必须使用Perspective显示模式（感觉戳到眼睛里）、虚化效果很差（采样率很低）、难以自定义效果。且必须自己尝试多次才能确定出合适的焦点深度。

为了解决这个问题我写了一个简单的程序辅助实现这一目的。
程序仅在Windows 8.1, 及最新的 VMD 1.9.3下测试并打包；不保证其他平台可用，但程序代码本身（除已存的程序路径外）是跨平台的、可以自行尝试。

效果图（请在较大屏幕上观看）：

![image](https://user-images.githubusercontent.com/18537705/160666682-6e8cad37-3248-4b9e-b3c0-a9dda7aeb210.png)
![image](https://user-images.githubusercontent.com/18537705/160666712-ef26c654-b797-4923-9a41-42d61fdc371a.png)




使用流程

准备工作：安装 VMD 1.9.3 和 POV-Ray 3.7 (程序包里已附带)，其中 POV-Ray 3.7 请安装到默认目录（否则自己找到并记住可执行文件 pvengine64.exe 的路径）

该程序支持VMD中可显示的任意表示方式，使用CPK表示完整分子时比较方便（其他情况（如蛋白的NewCartoon方式）在本文最后说明）。
首先在VMD中调整出想要的样子。如下图所示，此处我们假设希望通过焦点模糊突出箭头所示的羰基。


![image](https://user-images.githubusercontent.com/18537705/160666776-23beb2f0-c1b8-47da-9977-9891e939431e.png)


打开程序，首先点击【Gen .pov Filename】按钮，程序会询问最终渲染图片的保存路径，正常命名即可。
（注：虽然程序本身其实无此限制，但为了改掉一些坏毛病，程序会检查并禁止路径中带有空格）

![image](https://user-images.githubusercontent.com/18537705/160666809-3c4aee45-b91c-4b3e-abba-1f1c92c94b06.png)



正确选择保存路径和文件名后，文件路径会自动被复制到剪切板中（不必Ctrl+C）

![image](https://user-images.githubusercontent.com/18537705/160666824-3164fd21-f949-4fdc-afef-8c0dd1285ce1.png)



此时打开VMD的渲染控制，按照程序界面上的说明，做如下设定：
1. 选择渲染器为POV-Ray 3.6
2. 清空Filename栏，并直接Ctrl+V （程序已将所需的路径复制到剪切板了）
3. 清空Render Command
4. 点击 Start Rendering

![image](https://user-images.githubusercontent.com/18537705/160666847-670ce736-841f-48ac-864d-cbad048c483c.png)



这个过程只产生渲染文件而不进行渲染，应该瞬间结束。
随后点击程序中的【Load VMD generated .pov file】按钮载入文件。


随后需确定焦点所在的位置。
程序通过原子位置、或几个原子的几何重心确定焦点位置。
通过 VMD 的 Pick 模式（快捷键为 P）可以方便的在命令行窗口读到所关心原子的序数，此处C=O的序数分别是 Molecule ID为 1 的分子的 25 和 26 号原子

![image](https://user-images.githubusercontent.com/18537705/160666927-ed21d2af-0aa0-45ce-9a5b-3986325f81ed.png)


将此信息按格式输入程序 [Focal atoms] 中:
完整写法为 [Molecule-ID]:[Representation-ID]:[atom_index]，对上述原子是 "1:0:25 1:0:26"（不含引号，下同）
如果 Molecule-ID = 0 或 Representation-ID = 0 可以省去
例如上面的分子 Molecule-ID = 1，不能省去，但体系只有一个Representation（在 VMD-Graphics-Representations 中观察），故可简写为 "1:25 1:26"

![image](https://user-images.githubusercontent.com/18537705/160666959-b0a6ef41-8a9f-4a1b-bcdc-a60e5f2382e3.png)


点击【Submit】按钮后即可开始渲染。如果 POV-Ray 未装在默认位置，请自行寻找其可执行文件并告诉程序，程序会予以记录，下次就不用选择了。
渲染效果如图：

![image](https://user-images.githubusercontent.com/18537705/160666993-58048757-42b2-4296-8948-946f2b3ad276.png)


程序进行渲染时有几个参数，数值可用鼠标滚轮调整。各参数的效果示例如下，懂一点摄影的话很容易理解：

Resolution：生成图像的分辨率。理论上支持无穷高的分辨率。若一开始不确定下面各参数的合适范围，可先渲染小图，再渲染高分辨的图片。另外程序提供一个不更改设置的情况下渲染低分辨图片的按钮，可用于快速预览。

![image](https://user-images.githubusercontent.com/18537705/160667019-13eed379-5c00-4614-92bc-291943419bd3.png)


Depth of view：景深。决定虚化的程度。相当于相机光圈：

![image](https://user-images.githubusercontent.com/18537705/160667058-f93b965c-18bc-4903-8306-f9ae83ab4d6e.png)


Depth of view = 50, 100, 200



Blur Sampling：每个模糊进行的采样数量，数值越大效果越“光滑”，但渲染时间也呈指数增加。相当于相机底片的ISO。超过85基本就完全没有颗粒感了，分辨率不十分高的时候70即可以接受。程序下方的Draft按钮即是使用很低的采样率实现快速渲染供预览使用。

![image](https://user-images.githubusercontent.com/18537705/160667098-382bc1a1-579e-42d2-ab97-a61b4d011afa.png)


Blur sampling = 1, 60, 70, 85（在2核4线程的笔记本上渲染分别耗时 1s, 16s, 35s, 2 min 4 s）


![image](https://user-images.githubusercontent.com/18537705/160667257-3e82c05d-183a-482e-9b5d-f27d4eb61fea.png)


使用低采样率预览的Draft按钮


Orthographicality：透视/正交投影间的渐变，数值越大越接近正交投影，数值越小越产生“戳到眼睛里”的感觉。相当于相机离物体的远近（长焦换鱼眼）


![image](https://user-images.githubusercontent.com/18537705/160667133-ce1abbe8-b1e8-4b3e-ab14-c744cc4f5e08.png)

Orthographicality = 100, 30, 2 (前两个切换着看会比较明显)


Field width：视野的宽度，相当于相机焦距，数值越小视野越小。相当于变焦镜头推拉。

![image](https://user-images.githubusercontent.com/18537705/160667178-c5398f39-0c0a-4fee-a735-2988be4b88de.png)


Field width = 20, 50, 100





若所需显示的模式不是“完整的、分子的CPK模式”

由于程序需要 CPK 模式在 POV-Ray 文件中产生球面的球心位置来定位焦点，故若分子不以 CPK 模式需要做如下调整：
以下图所示 NewCartoon 方式显示的蛋白为例

![image](https://user-images.githubusercontent.com/18537705/160667331-f253681c-038c-49ce-b705-e1f62a39ffdf.png)


1. 调好所有效果后，最后在VMD中创建一个以 CPK模式显示的、完整分子的（Selected Atom = All）Representation

![image](https://user-images.githubusercontent.com/18537705/160667375-066e5460-b5c4-418e-96eb-2f7ca8576505.png)


2. 记录这个多余的Representation的序号（从0开始），此处为 1
3. 正常查看所需焦点的原子序号，如此处所指为 2 号分子的 869号 原子
![image](https://user-images.githubusercontent.com/18537705/160667440-4189e702-9d3f-422d-b8ea-af1decbb29f2.png)


4. 按完整格式填写焦点原子 （[Molecule-ID]:[Representation-ID]:[atom_index]），此处为 2:1:869

5. 【关键】：在 [Remove CPK Molecules] 一栏中填入需要删除的、之前多余的 CPK Representation，格式为（[Molecule-ID]:[Representation-ID]），此处为 2:1

6. 其他参数正常设置，提交。

![image](https://user-images.githubusercontent.com/18537705/160667475-9548059c-bc63-4bae-a693-7d7beb2e1350.png)



得到效果如图

![image](https://user-images.githubusercontent.com/18537705/160667505-12a6e897-e37d-4735-ad0e-02fcd2e96aa7.png)




Bug report

这是一个自用程序，我用VMD大多是显示小分子，故可能未考虑到一些我不使用的情况。

已知的问题：
效率：Submit 大分子（数千原子）时较慢，约需几秒，因为此处渲染过程完全是决速步，故而暂未打算优化，稍等片刻即可。
参数正交性：各参数已经过变换，使得调整相应量时尽量不相互依赖，但由于使用了一些近似（诸如小角时 sin(x)=x），如果把参数调的特别离谱时，可能调整一个参数也连带需要调整另一参数，多加尝试即可。

遇到Bug时，请提供：
1. 载入VMD的结构文件
2. VMD中“File-Save visualization state”功能产生的状态文件。
3. 本程序界面（GUI）截图
4. 如果程序崩溃，提供本程序附带的CMD窗口（黑窗口）的截图

更新

20170406： 增加了一个“Draft”按钮，用来自动以低质量生成图片用于预览（在一般电脑上一般1~2秒即可渲染完的低质量图片）用于调试参数。

![image](https://user-images.githubusercontent.com/18537705/160667544-03d80a97-48a4-40b7-87c9-154f19686039.png)
