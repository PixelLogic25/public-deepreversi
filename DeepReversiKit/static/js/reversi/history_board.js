
class HistoryBoard{
constructor(){
    this.history = new Array();
    this.idHistory = new Array();

}

push_move(board,index){
    
    this.history.splice(index,0,board)
    if (!isElementAtIndex(this.idHistory,index)){
        //存在しないのでid新規作成
        this.idHistory.splice(index,0,[0]);
    }else{
        this.idHistory[index].push(this.idHistory[index].length);

    }

}


}