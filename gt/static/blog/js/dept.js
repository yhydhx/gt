var school={
	"UESTC":0,
	"AAA":1,
	"BBB":2,
	"CCC":3,
};
var dept={
	"complexLab":0,
	"bigData":0,
	"tmpA":1,
	"YT":1,
	"tmpB":2,
	"tmpC":3,
};
var deptNames=[
	"complexLab",
	"bigData",
	"tmpA",
	"YT",
	"tmpB",
	"tmpC",
];
var deptIndex={
	"complexLab":0,
	"bigData":1,
	"tmpA":2,
	"YT":3,
	"tmpB":4,
	"tmpC":5,
};
var deptIndexS={
	"complexLab":0,
	"bigData":1,
	"tmpA":0,
	"YT":1,
	"tmpB":0,
	"tmpC":0,
};
var schoolList=["UESTC","AAA","BBB","CCC"];
var schoolOffset = [0,2,4,5,6];
function getSchoolName(departmentName){    return schoolList[dept[departmentName]];}
function getSchoolIndex(departmentName) {    return dept[departmentName];}