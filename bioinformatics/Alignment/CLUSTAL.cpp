#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
#include <vector>                          
#include <iterator> 
#include <ctime>
//#include <windows.h>
//声明命名空间std
using namespace std;
#define MATCH 1
#define DIS_MATCH -1
#define INDEL -3
#define INDEL_CHAR '-'
// 代码来源  https://blog.csdn.net/baidu_41860619/article/details/118071986
class ResUnit {		//一次双序列比对后的结果
public:
	string str1;	//原始序列1
	string str2;	//原始序列2
	string res1;	//结果序列1
	string res2;	//结果序列2
	int score;		//序列总得分，反映两个序列的相似程度
	int tag;		//禁止迭代多次
};

class SingleSeq {	//一个序列被整合后的样子
public:
	string str;		//一个序列的原始序列
	string res;		//一个序列被整合后的样子

};

struct BacktrackingUnit {
	int goUp;		//是否向上回溯
	int goLeftUp;	//是否向左上回溯
	int goLeft;		//是否向左回溯
	int score;		//得分矩阵第(i, j)这个单元的分值
};


typedef struct BacktrackingUnit *unitLine;

int max3(int a, int b, int c);
int myCompare(char a, char b);
ResUnit traceback(unitLine** item, const int i, const int j, string str1, string str2, string res1, string res2, int n, ResUnit resUnit);
ResUnit NeedlemanWunch(string str1, string str2);
void getResUnitMatrix(string *s, int length, ResUnit **res);
int ifStrInQueueFinish(string str, vector<SingleSeq> queue_finish);
vector<SingleSeq> RegularTwo(ResUnit tag, ResUnit temp, vector<SingleSeq> queue_finish);
vector<SingleSeq> RegularSeq1(ResUnit tag, vector<SingleSeq> queue_finish, int item);
vector<SingleSeq> RegularSeq2(ResUnit tag, vector<SingleSeq> queue_finish, int item);

struct SequenceUnit {
	string *str1;	//匹配序列1
	string *str2;	//匹配序列2
	int score;
};

bool complare(const ResUnit &a, const ResUnit &b)
{
	return a.score > b.score;
}


//主方法入口
int main() {
	clock_t startTime, endTime;
	startTime = clock();//计时开始

	//clust算法
	const int sequence_groups = 7;
	string *ss = new string[sequence_groups];
	ss[0] = "ACCTTGGGAAAATTCCGGGACA";
	ss[1] = "AACGGAAAATTCCGGGACCTT";
	ss[2] = "AATTCCGGAATTCCGGGACA";
	ss[3] = "AATTCGGAAAATTCCGGGACA";
	ss[4] = "AATTCCGGAAAATTCCGACA";
	ss[5] = "AACCCGGAAAATTCCGGGACA";
	ss[6] = "AATTCCGGAAAACTCGGGACA";
	// ss[7] = "AATGGAAAATTCCGCGGCA";
	// ss[8] = "AATGTCCGGAAAATTCCGGGACA";
	// ss[9] = "ATGCGGAAAATTCCCAAGGGACA";
	// ss[10] = "AATCGGAAATTATTCCGGGACA";
	// ss[11] = "CCTCCCGGATTCCGGGAGCA";
	// ss[12] = "AACTGCGGAAAATTCCGGGACA";
	// ss[13] = "AATTCCGGAAAATTCCGGATCCA";
	// ss[14] = "AATATCCGAAAATTCCGGGACA";
	// ss[15] = "AATTCCGGAAAATCCATCCACA";
	// ss[16] = "AATCGGAAAATTCGGGACA";
	// ss[17] = "AACCGGAAAATTCCCCTGGGACA";
	// ss[18] = "ATTTCCGGAAATTCCGGGACA";
	// ss[19] = "AATTCCGGAAATTCCGGCCACA";
	// ss[20] = "AAGGCGGAAAATTCGCCGGACA";
	// ss[21] = "AATGGCGAAAATTCCGGGACA";
	// ss[22] = "AATCCGGAAAATTCCTCCACA";
	// ss[23] = "AATTTCGGGAAAATTCCGGGACA";
	// ss[24] = "AATTCCGGAAAATTCCGGGCTACA";
	// ss[25] = "AACCTCGGAAAATTCCGGGACA";
	// ss[26] = "AATTAACCGGAAAATGGGGACA";
	// ss[27] = "ACCATCCGGAAAATTCCGGGACA";
	// ss[28] = "AATTCCGGAAAATTCATGCGGACA";
	// ss[29] = "AATTCCCATGAAAATTCCGGGACA";
	// ss[30] = "AACCTAGGAAAATTCCGGGACA";

	vector<ResUnit> queue_initial(0); //定义等待整合的队列，是一个ResUnit对象vector
	vector<SingleSeq> queue_finish(0); //定义整合完毕的队列，是一个String类型的vector
	vector<ResUnit>::iterator it; //迭代器，访问queue_initial
	vector<SingleSeq>::iterator it_finish;  //迭代器，访问queue_finish

											//结果矩阵，，二维向量
	ResUnit **res;
	res = new ResUnit*[sequence_groups];
	for (int i = 0; i < sequence_groups; i++)
	{
		res[i] = new ResUnit[sequence_groups];
		for (int j = 0; j < sequence_groups;j++) {
			res[i][j] = ResUnit();
		}
	}

	getResUnitMatrix(ss, sequence_groups, res);

	//开始多序列比对
	//定义队列长度
	int queue_length = ((sequence_groups - 1)*sequence_groups) / 2;
	cout << "queue_length:" << queue_length << endl;

	//将res内元素放入等待整合队列--按分数从高到低排列
	for (int i = 0;i < sequence_groups;i++) {
		for (int j = i + 1;j < sequence_groups;j++) {
			//放入容器
			queue_initial.push_back(res[i][j]);
		}
	}
	// for (it = queue_initial.begin();it != queue_initial.end();it++) {
		
	// 	cout << "it->res2:" << it->res2 << endl;
	// 	cout << "it->res1:" << it->res1 << endl;
	// 	cout << "it->score:" << it->score << endl;
	// }
	//排序
	sort(queue_initial.begin(), queue_initial.end(), complare);
	// for (it = queue_initial.begin();it != queue_initial.end();it++) {
		
	// 	cout << "it->res2:" << it->res2 << endl;
	// 	cout << "it->res1:" << it->res1 << endl;
	// 	cout << "it->score:" << it->score << endl;
	// }
	//最多循环queue_length次
	for (int i = 0;i < queue_length;i++) {
		//当结果队列长度与sequence_groups相等之后，就说明全部放入了结果队列，可以跳出循环了
		if (sequence_groups == queue_finish.size())
			break;

		//一个ResUnit对象的str1属性和str2均不在
		if (ifStrInQueueFinish(queue_initial.at(i).str1, queue_finish) < 0 && \
		ifStrInQueueFinish(queue_initial.at(i).str2, queue_finish) < 0) {
			SingleSeq singleSeq1, singleSeq2;
			singleSeq1.str = queue_initial.at(i).str1;
			singleSeq1.res = queue_initial.at(i).res1;
			singleSeq2.str = queue_initial.at(i).str2;
			singleSeq2.res = queue_initial.at(i).res2;

			//如果结果队列已经有元素，，且又来了俩不相干的，却很匹配的序列对
			if (queue_finish.size()>0) {

				//将结果队列第一个的序列和queue_initial.at(i).str1进行双序列比对
				ResUnit temp = NeedlemanWunch(queue_finish.front().str, queue_initial.at(i).str1);
				//进行规整操作
				queue_finish = RegularTwo(queue_initial.at(i), temp, queue_finish);
			}
			else
			{
				queue_finish.push_back(singleSeq1);
				queue_finish.push_back(singleSeq2);
			}

		}
		//str1在，str2不在
		else if (ifStrInQueueFinish(queue_initial.at(i).str1, queue_finish) > -1 && \
		ifStrInQueueFinish(queue_initial.at(i).str2, queue_finish) < 0) {
			int item = ifStrInQueueFinish(queue_initial.at(i).str1, queue_finish);
			queue_finish = RegularSeq1(queue_initial.at(i), queue_finish, item);
		}
		//str2在，str1不在
		else if (ifStrInQueueFinish(queue_initial.at(i).str2, queue_finish) > -1 && \
		ifStrInQueueFinish(queue_initial.at(i).str1, queue_finish) < 0) {
			int item = ifStrInQueueFinish(queue_initial.at(i).str2, queue_finish);
			queue_finish = RegularSeq2(queue_initial.at(i), queue_finish, item);
		}
	}


	//声明一个迭代器，来访问vector容器
	
	cout << "--------------------------------------------------------------------" << endl;
	cout << endl << "原序列" << endl<< endl;
	for (it_finish = queue_finish.begin();it_finish != queue_finish.end();it_finish++) {
		cout << "  " << it_finish->str << endl;
	}
	cout << endl<< endl << "比对后" << endl << endl;
	for (it_finish = queue_finish.begin();it_finish != queue_finish.end();it_finish++) {
		cout <<"  "<< it_finish->res << endl;
	}
	
	endTime = clock();//计时结束
	cout << endl << endl << "The run time is: " << (double)(endTime - startTime) / CLOCKS_PER_SEC << "s" << endl;
	cout << "--------------------------------------------------------------------" << endl;
	system("pause");
	return 0;
}

/*
规整函数，规整两个序列情况

queue_finish      temp		tag
A1				  A2		E1
B				  E2		F
C
D
*/
vector<SingleSeq> RegularTwo(ResUnit tag, ResUnit temp, vector<SingleSeq> queue_finish) {
	string E2 = temp.res2;
	string E1 = tag.res1;
	string A1 = queue_finish.front().res;
	string A2 = temp.res1;
	string F = tag.res2;
	string tempStr = "";
	vector<SingleSeq>::iterator it;//声明一个迭代器，来访问vector容器

	int i = 0, j = 0;
	//第一步，，整合tag与temp
	while (E2 != E1 && j < E1.length() && i < E2.length()) {
		if (E2[i] == E1[j]) {
			i++;
			j++;
		}
		else {
			if (E2[i] == '-') {
				E1.insert(j, "-");
				F.insert(j, "-");

			}
			else if (E1[j] == '-')
			{
				E2.insert(i, "-");
				A2.insert(i, "-");

			}
		}
	}

	if (i == E2.length()) {

		//E2先到头
		for (int k = 0; k < E1.length() - j; k++)
		{
			tempStr += "-";
		}
		E2 += tempStr;
		A2 += tempStr;

	}
	else if (j == E1.length()) {
		//E1先到头
		for (int k = 0; k < E2.length() - i; k++)
		{
			tempStr += "-";
		}
		E1 += tempStr;
		F += tempStr;
	}

	//将tempStr置空
	tempStr = "";

	//第二步 融合进queue_finish
	i = 0, j = 0;
	while (A1 != A2 && i < A1.length() && j < A2.length()) {
		if (A1[i] == A2[j]) {
			i++;
			j++;
		}
		else {
			if (A1[i] == '-') {
				A2.insert(j, "-");
				E1.insert(j, "-");
				F.insert(j, "-");
			}
			else if (A2[j] == '-')
			{
				A1.insert(i, "-");
				for (it = queue_finish.begin();it != queue_finish.end();it++) {
					it->res = it->res.insert(i, "-");
				}
			}
		}
	}

	if (i == A1.length()) {

		//A1先到头
		for (int k = 0; k < A2.length() - j; k++)
		{
			tempStr += "-";
		}
		A1 += tempStr;
		for (it = queue_finish.begin();it != queue_finish.end();it++) {
			it->res = it->res + tempStr;
		}

	}
	else if (j == A2.length()) {
		//A2先到头
		for (int k = 0; k < A1.length() - i; k++)
		{
			tempStr += "-";
		}
		A2 += tempStr;
		E1 += tempStr;
		F += tempStr;
	}

	//规划好之后，，将 E F 插入queue_finish尾部
	SingleSeq sE, sF;
	sE.res = E1;
	sE.str = tag.str1;
	sF.res = F;
	sF.str = tag.str2;
	queue_finish.push_back(sE);
	queue_finish.push_back(sF);
	return queue_finish;
}

/*
规整函数，规整序列1情况

queue_finish      tag
A1				  A2
B				  E
C
D
*/
vector<SingleSeq> RegularSeq1(ResUnit tag, vector<SingleSeq> queue_finish, int item) {
	SingleSeq main_seq = queue_finish.at(item);//找到和seq1相同的序列
	string A1 = main_seq.res;
	string A2 = tag.res1;
	string E = tag.res2;
	string tempStr = "";
	vector<SingleSeq>::iterator it;//声明一个迭代器，来访问vector容器
	int i = 0, j = 0;
	while (A1 != A2 && i < A1.length() && j < A2.length()) {
		if (A1[i] == A2[j]) {
			i++;
			j++;
		}
		else {
			if (A1[i] == '-') {
				A2.insert(j, "-");
				E.insert(j, "-");
			}
			else if (A2[j] == '-') {
				//遍历queue_finish,给queue_finish内res洗头
				A1.insert(i, "-");
				for (it = queue_finish.begin();it != queue_finish.end();it++) {
					it->res = it->res.insert(i, "-");
				}
			}
		}
	}

	if (i == A1.length()) {

		//A1先到头
		for (int k = 0; k < A2.length() - j; k++)
		{
			tempStr += "-";
		}
		A1 += tempStr;
		for (it = queue_finish.begin();it != queue_finish.end();it++) {
			it->res = it->res + tempStr;
		}

	}
	else if (j == A2.length()) {
		//A2先到头
		for (int k = 0; k < A1.length() - i; k++)
		{
			tempStr += "-";
		}
		A2 += tempStr;
		E += tempStr;
	}

	//添加
	SingleSeq sE;
	sE.res = E;
	sE.str = tag.str2;
	queue_finish.push_back(sE);
	return queue_finish;
}

/*
规整函数，规整序列2情况

queue_finish      tag
A1				  E
B				  A2
C
D
*/
vector<SingleSeq> RegularSeq2(ResUnit tag, vector<SingleSeq> queue_finish, int item) {
	SingleSeq main_seq = queue_finish.at(item);//找到和seq1相同的序列
	string A1 = main_seq.res;
	string A2 = tag.res2;
	string E = tag.res1;
	string tempStr = "";
	vector<SingleSeq>::iterator it;//声明一个迭代器，来访问vector容器

	int i = 0, j = 0;
	while (A1 != A2 && i < A1.length() && j < A2.length()) {
		if (A1[i] == A2[j]) {
			i++;
			j++;
		}
		else {
			if (A1[i] == '-') {
				A2.insert(j, "-");
				E.insert(j, "-");
			}
			else if (A2[j] == '-') {
				//遍历queue_finish,给queue_finish内res洗头
				A1.insert(i, "-");
				for (it = queue_finish.begin();it != queue_finish.end();it++) {
					it->res = it->res.insert(i, "-");
				}
			}
		}
	}

	if (i == A1.length()) {

		//A1先到头
		for (int k = 0; k < A2.length() - j; k++)
		{
			tempStr += "-";
		}
		A1 += tempStr;
		for (it = queue_finish.begin();it != queue_finish.end();it++) {
			it->res = it->res + tempStr;
		}

	}
	else if (j == A2.length()) {
		//A2先到头
		for (int k = 0; k < A1.length() - i; k++)
		{
			tempStr += "-";
		}
		A2 += tempStr;
		E += tempStr;
	}
	//添加
	SingleSeq sE;
	sE.res = E;
	sE.str = tag.str1;
	queue_finish.push_back(sE);
	return queue_finish;
}


//判断一个str是否有与queue_finish数组对象内的seq相等的,没有返回-1,有就返回序号
int ifStrInQueueFinish(string str, vector<SingleSeq> queue_finish) {
	int i = 0;
	vector<SingleSeq>::iterator it;//声明一个迭代器，来访问vector容器
	for (it = queue_finish.begin();it != queue_finish.end();it++) {
		if (str == it->str)
			return i;
		i++;
	}
	return -1;
}


/**
循环比较一组序列的值，返回一个ResUnit对象数组，二维，且是个倒三角形状
其中，s是一个字符串类型的数组，存储等待序列比对的一组数据
*/
void getResUnitMatrix(string *s, int length, ResUnit **res) {

	int sLength = length;
	cout << "sLength:" << sLength << endl;
	if (sLength == 1)
	{
		cout << "不符合输入规范" << endl;
	}

	for (int i = 0;i < sLength;i++) {
		for (int j = i + 1;j < sLength;j++) {
			//只遍历上三角区域
			res[i][j] = NeedlemanWunch(s[i], s[j]);
		}
	}
}

/**
比较三种路径之间谁最大

f(i-1,j-1),f(i-1,j)+indel,f(i,j-1)+indel
*/
int max3(int a, int b, int c) {
	int temp = a > b ? a : b;
	return temp > c ? temp : c;
}

/**
比较两个字符类型属于什么，match，dismatch，indel
*/
int myCompare(char a, char b) {
	if (a == b)
		return MATCH;
	else if (a == ' ' || b == ' ')
		return INDEL;
	else
		return DIS_MATCH;
}


ResUnit traceback(unitLine** item, const int i, const int j, string str1, string str2, string res1, string res2, int n, ResUnit resUnit) {
	unitLine temp = item[i][j];
	if (resUnit.tag != 1)
	{
		if (!(i || j)) {   // 到矩阵单元(0, 0)才算结束，这代表初始的两个字符串的每个字符都被比对到了

			resUnit.str1 = str1;
			resUnit.str2 = str2;
			resUnit.res1 = res1;
			resUnit.res2 = res2;
			resUnit.tag = 1;
			return resUnit;
		}
		if (temp->goUp) {    // 向上回溯一格
			res1 = str1[i - 1] + res1;
			res2 = INDEL_CHAR + res2;
			resUnit = traceback(item, i - 1, j, str1, str2, res1, res2, n + 1, resUnit);
		}
		if (temp->goLeftUp) {    // 向左上回溯一格 
			res1 = str1[i - 1] + res1;
			res2 = str2[j - 1] + res2;
			resUnit = traceback(item, i - 1, j - 1, str1, str2, res1, res2, n + 1, resUnit);
		}
		if (temp->goLeft) {    // 向左回溯一格
			res1 = INDEL_CHAR + res1;
			res2 = str2[j - 1] + res2;
			resUnit = traceback(item, i, j - 1, str1, str2, res1, res2, n + 1, resUnit);
		}
		return resUnit;
	}
	else
	{
		return resUnit;
	}

}


ResUnit NeedlemanWunch(string str1, string str2) {
	//字符串str1,str2长度
	const int m = str1.length();
	const int n = str2.length();

	int m1, m2, m3, mm;

	unitLine **unit;

	// 初始化
	if ((unit = (unitLine **)malloc(sizeof(unitLine*) * (m + 1))) == NULL) {
		fputs("Error: Out of space!\n", stderr);
		exit(1);
	}
	for (int i = 0; i <= m; i++) {
		if ((unit[i] = (unitLine *)malloc(sizeof(unitLine) * (n + 1))) == NULL) {
			fputs("Error: Out of space!\n", stderr);
			exit(1);
		}
		for (int j = 0; j <= n; j++) {
			if ((unit[i][j] = (unitLine)malloc(sizeof(struct BacktrackingUnit))) == NULL) {
				fputs("Error: Out of space!\n", stderr);
				exit(1);
			}
			unit[i][j]->goUp = 0;
			unit[i][j]->goLeftUp = 0;
			unit[i][j]->goLeft = 0;
		}
	}
	unit[0][0]->score = 0;
	for (int i = 1; i <= m; i++) {
		unit[i][0]->score = INDEL * i;
		unit[i][0]->goUp = 1;
	}
	for (int j = 1; j <= n; j++) {
		unit[0][j]->score = INDEL * j;
		unit[0][j]->goLeft = 1;
	}


	// 动态规划算法计算得分矩阵每个单元的分值
	for (int i = 1; i <= m; i++) {
		for (int j = 1; j <= n; j++) {
			m1 = unit[i - 1][j]->score + INDEL;
			m2 = unit[i - 1][j - 1]->score + myCompare(str1[i - 1], str2[j - 1]);
			m3 = unit[i][j - 1]->score + INDEL;
			mm = max3(m1, m2, m3);
			unit[i][j]->score = mm;
			//判断路径来源
			if (m1 == mm) unit[i][j]->goUp = 1;
			if (m2 == mm) unit[i][j]->goLeftUp = 1;
			if (m3 == mm) unit[i][j]->goLeft = 1;
		}
	}


	//开始回溯
	ResUnit res;
	res.tag = 0;
	res = traceback(unit, m, n, str1, str2, "", "", 0, res);
	res.score = unit[m][n]->score;


	//释放内存
	for (int i = 0; i <= m; i++) {
		for (int j = 0; j <= n; j++) {
			free(unit[i][j]);
		}
		free(unit[i]);
	}
	free(unit);

	//返回值
	return res;
}
