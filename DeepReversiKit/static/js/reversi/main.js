

$(document).ready(function() {
    $('.cell').click(function() {
        var x = $(this).data('x');
        var y = $(this).data('y');
        
        if (mainReversiGame.possible_move_array[x+y*8]){
            move(x, y);
        }
    });
});

async function move(x,y){

    if (!sysControl.isPossiblePlayerMove){
        //今は盤面に石を置くことができない。
        return
    }

    //試合中でCPUの番なら無効
    if (sysControl.isGamePlaying && 
        (sysControl.isFirstCpuFlag == mainReversiGame.board.turn || 
            sysControl.isSecondCpuFlag == !mainReversiGame.board.turn)){

        return
    }


    //置くことができるというなら最速で置けなくさせる。
    sysControl.isPossiblePlayerMove=false;
    
    
    mainRecoardCenterProccess.add(y*8+x,mainReversiGame);
    //盤面の更新
    mainBoard.updateBoard([y*8+x]);
    //石の個数更新
    guiControl.updateCountStone(mainReversiGame.getBlackStouneCount(),mainReversiGame.getWhiteStouneCount());


    //cpuの手を必要なら求める
    cpuMove();

    



    //盤面のロックを解除
    sysControl.isPossiblePlayerMove=true;
}

//対戦開始時
function game_start(){

    cpuMove();
    //盤面のロックを解除
    sysControl.isPossiblePlayerMove=true;
}

//cpuが手を打つべきかを判断して、必要ならCPUが手を打つ
async function cpuMove(aiAskButtonPushed) {

    sysControl.cpuNowThinking = true;
    //cpuの手番なら通信をして手番を取得する。
    while(
        !sysControl.isErrorStop && //エラーが発生していないならtrue
        (sysControl.isGamePlaying || aiAskButtonPushed) && //対戦中か、Aiに聞くボタンが押されたならtrue
        !mainReversiGame.isGameEnd() && //終了盤面ならfalse
        (aiAskButtonPushed || //Aiに聞いたなら手番関係なく打つ
            ((sysControl.isFirstCpuFlag && mainReversiGame.board.turn) || //先手CPUが有効ならtrue
             (sysControl.isSecondCpuFlag && !mainReversiGame.board.turn)))//後手CPUが有効ならtrue
            ){
        await reversiSendReceive.sendAskCpu(mainReversiGame,sysControl.deep_num).then(move=> {
            if (move!=-1){
                mainRecoardCenterProccess.add(move,mainReversiGame);//cpuが手を打つ
                mainBoard.updateBoard([move]);

                //石の個数表示の更新
                guiControl.updateCountStone(mainReversiGame.getBlackStouneCount(),mainReversiGame.getWhiteStouneCount());
                //手番の表示を更新
                guiControl.update_now_turn_display(mainRecoardCenterProccess.game.board.turn);
            }else{
                sysControl.isErrorStop = true;
                alert('サーバーとの通信に失敗しました');
            }
        });

        aiAskButtonPushed = false;//一手打ったらfalseにする。さもないと無限に打つ。
    }


    guiControl.updateCountStone(mainReversiGame.getBlackStouneCount(),mainReversiGame.getWhiteStouneCount());
    guiControl.update_now_turn_display(mainReversiGame.board.turn);

    guiControl.mainRecordSelectIndex = mainRecoardCenterProccess.mainData[mainRecoardCenterProccess.nowUuid].turn_num;
    guiControl.updateSelectElement();//棋譜のセレクトボックスの更新

    if (sysControl.isErrorStop){
        if (sysControl.isGamePlaying){
            guiControl.gamePause();
        }
        sysControl.isErrorStop=false;
    }

    sysControl.cpuNowThinking = false;
}

//ページが読み込まれた直後に行う処理
function JavascriptInit() {


    
    
    mainReversiGame = new ReversiGame();


    mainBoard = new MainBoard();

    mainBoard.CreateBoard();
    mainBoard.updateBoard();

    mainRecoardCenterProccess = new MainBoardCenterProcess(mainReversiGame,mainBoard);//棋譜の記録をする。分岐する棋譜もここで管理をする


    sysControl = new SystemControl();
    saveLoad = new SaveLoad(sysControl);
    guiControl = new GuiControl(sysControl);
    reversiSendReceive = new ReversiSendReceive(sysControl);

    sysControl.setClassData(mainRecoardCenterProccess,mainBoard,mainReversiGame,saveLoad,guiControl,reversiSendReceive);

   

    guiControl.isSecondCpuCheckBox.checked = sysControl.isSecondCpuFlag;

    guiControl.updateSelectElement();

    
    arrow_cot = new ArrowControl();
    
}




var board_data =[];
var move_posible = [];
var now_turn = true;
var black_num =2;
var white_num =2;
// ページが読み込まれた後にボードを生成
document.addEventListener('DOMContentLoaded', JavascriptInit);