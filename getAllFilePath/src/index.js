const fs = require('fs');
const path = require('path');

// let fileList = [];
///////////////////////////////////////////////////////////////////////////
// pending
// const getFileList = function (filePath) {
//     let fileList = [];
//     return new Promise(function (resolve,reject) {
//         fs.readdir(filePath,function(err,files){
//             if(err){
//                 console.warn(err)
//                 return reject(err)
//             }else{
//                 //遍历读取到的文件列表
//                 files.forEach(function(filename){
//                     //获取当前文件的绝对路径
//                     var filedir = path.join(filePath, filename);

//                     const stat = fs.statSync(filedir);

//                     if(stat.isFile()){
//                         fileList.push(filedir);
                        
//                         // console.log(filedir);
//                     }
//                     if(stat.isDirectory()){
//                         getFileList(filedir);//递归，如果是文件夹，就继续遍历该文件夹下面的文件
//                     }
//                 });
//                 resolve(fileList);
//             }
            
//         });
//     })
// }



// const get = async () => {

//     const basePath1 =  'C:\\Mine\\me\\my-elm\\src';

//     const basePath2 =  'C:\\Mine\\me\\react-elm-master\\src';
//     console.log('-------------fileList1------------')
//     let list1 = await getFileList(basePath1);
//     console.log(list1);

//     console.log('-------------fileList2------------')
//     let list2 = await getFileList(basePath2);
//     console.log(list2);

// };

// get();

//////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////
// org
//文件遍历方法
// function getFileList1(filePath){
//     //根据文件路径读取文件，返回文件列表
//     fs.readdir(filePath,function(err,files){
//         if(err){
//             console.warn(err)
//         }else{
//             //遍历读取到的文件列表
//             files.forEach(function(filename){
//                 //获取当前文件的绝对路径
//                 var filedir = path.join(filePath, filename);
//                 //根据文件路径获取文件信息，返回一个fs.Stats对象
//                 fs.stat(filedir,function(eror, stats){
//                     if(eror){
//                         console.warn('获取文件stats失败');
//                     }else{
//                         var isFile = stats.isFile();//是文件
//                         var isDir = stats.isDirectory();//是文件夹
//                         if(isFile){
//                             fileList.push(filedir);
//                             console.log(filedir);
//                         }
//                         if(isDir){
//                             getFileList(filedir);//递归，如果是文件夹，就继续遍历该文件夹下面的文件
//                         }
//                     }
//                 })
//             });
//         }
//     });
// }
//////////////////////////////////////////////////////////////////////


function getAllFileSync(filePath,fileList) {
    fs.readdirSync(filePath).forEach(fileName => {
        let fileDir = path.join(filePath,fileName);
        const stat = fs.statSync(fileDir);
        if (stat.isFile()){
            fileList.push(fileDir);
        }
        if(stat.isDirectory()){
            getAllFileSync(fileDir,fileList);
        }
    });
    return fileList;
}

const basePath1 =  'C:\\Mine\\me\\my-elm\\src';

const basePath2 =  'C:\\Mine\\me\\react-elm-master\\src';
let tempList1 = [];
let tempList2 = [];
console.log('-------------fileList1------------')
var list1 = getAllFileSync(basePath1,tempList1);
console.log(list1);

console.log('-------------fileList2------------')
var list2 = getAllFileSync(basePath2,tempList2);
console.log(list2);
