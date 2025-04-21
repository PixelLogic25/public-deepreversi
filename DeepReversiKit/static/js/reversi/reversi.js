
//ページの読み込み時の処理
$(document).ready(function() {
    $('.cell').click(function() {
        var x = $(this).data('x');
        var y = $(this).data('y');
        
        if (move_posible[x+y*8]==1){
            sendMove(x, y);
        }
    });

    function sendMove(x, y) {
        $.ajax({
            url: '/move',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({x: x, y: y}),
            success: function(response) {
                //alert('Move successful: ' + response.result);
                
                const tmp_board_str = response.b;
                
                //おける場所更新
                move_posible =[];
                tmp_index = 0;
                for(let i=0;i<response.move_posible.length;i++){
                    move_posible[response.move_posible[i]]=1;
                }

                //ボードデータ更新
                board_data = tmp_board_str.split(",").map(function(item) {
                    return parseInt(item, 10); // 10は基数で、10進数を示します
                });

                now_turn = response.turn;

                black_num = response.b_num;
                white_num = response.w_num;
                updateBoard();
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    }
});



function sendUpdate(resetFlag,backFlag,fowardFlag) {
    $.ajax({
        url: '/update',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({reset:resetFlag,back:backFlag,foward:fowardFlag}),
        success: function(response) {
            //alert('Move successful: ' + response.result);
            
            const tmp_board_str = response.b;
            
            //おける場所更新
            move_posible =[];
            tmp_index = 0;
            for(let i=0;i<response.move_posible.length;i++){
                move_posible[response.move_posible[i]]=1;
            }

            //ボードデータ更新
            board_data = tmp_board_str.split(",").map(function(item) {
                return parseInt(item, 10); // 10は基数で、10進数を示します
            });

            now_turn = response.turn;

            black_num = response.b_num;
            white_num = response.w_num;
            updateBoard();
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

function sendGenerate(){
    $.ajax({
        url: '/edit',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({board:document.getElementById('edit_board').value}),
        success: function(response) {
            //alert('Move successful: ' + response.result);
            
            const tmp_board_str = response.b;
            
            //おける場所更新
            move_posible =[];
            tmp_index = 0;
            for(let i=0;i<response.move_posible.length;i++){
                move_posible[response.move_posible[i]]=1;
            }

            //ボードデータ更新
            board_data = tmp_board_str.split(",").map(function(item) {
                return parseInt(item, 10); // 10は基数で、10進数を示します
            });

            now_turn = response.turn;

            black_num = response.b_num;
            white_num = response.w_num;
            updateBoard();
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });

}

function sendBoardHistoryMoves(){
    $.ajax({
        url: '/moves_history',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({moves:document.getElementById('edit_board_by_moves').value}),
        success: function(response) {
            //alert('Move successful: ' + response.result);
            
            const tmp_board_str = response.b;
            
            //おける場所更新
            move_posible =[];
            tmp_index = 0;
            for(let i=0;i<response.move_posible.length;i++){
                move_posible[response.move_posible[i]]=1;
            }

            //ボードデータ更新
            board_data = tmp_board_str.split(",").map(function(item) {
                return parseInt(item, 10); // 10は基数で、10進数を示します
            });

            now_turn = response.turn;


            black_num = response.b_num;
            white_num = response.w_num;
            updateBoard();
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });

}


function updateBoard() {
    
    const board = document.getElementById('reversi-board');
    const row = board.getElementsByClassName('row');

    const block_stone_num = document.getElementById('black-count');
    const white_stone_num = document.getElementById('white-count');



    for (let y = 0; y < 8; y++) {
        
        const cell = row[y].getElementsByClassName('cell');
        for (let x = 0; x < 8; x++) {
            cell[x].removeChild(cell[x].firstChild);
        }
        for (let x = 0; x < 8; x++) {
            const cell_data = document.createElement('div');
            cell_data.className = 'none';

            if (board_data[x+y*8]==-1){
                cell_data.className = 'black';
            }
            if (board_data[x+y*8]==1){
                cell_data.className = 'white';
            }
            if (move_posible[y*8+x]==1){
                cell_data.className = 'possible';

            }

            cell[x].appendChild(cell_data);
        }
    }

    let color = "";
    if (now_turn){
        color = "黒";
    }else{
        color = "白";
    }


    document.getElementById('now-turn').textContent = color;


    block_stone_num.textContent =""+black_num;
    white_stone_num.textContent =""+white_num;
}


function JavascriptInit() {

    document.getElementById('resetButton').addEventListener('click', function() {
        sendUpdate(true,false,false);
    });


    document.getElementById('backButton').addEventListener('click', function() {
        sendUpdate(false,true,false);
    });

    document.getElementById('fowardButton').addEventListener('click', function() {
        sendUpdate(false,false,true);
    });

    document.getElementById('editButton').addEventListener('click', function() {
        sendGenerate();
    });

    document.getElementById('movesButton').addEventListener('click', function() {
        sendBoardHistoryMoves();
    });


    CreateBoard();
    sendUpdate(false,false,false);
}

function CreateBoard(){
    const board = document.getElementById('reversi-board');
    for (let y = 0; y < 8; y++) {
        const row = document.createElement('div');
        row.className = 'row';
        for (let x = 0; x < 8; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';

            const cell_data = document.createElement('div');
            cell_data.className = 'none';

            /*
            if (x == 3 && y==3){
                cell_data.className = 'white';
            }
            if (x == 4 && y==4){
                cell_data.className = 'white';
            }
            if (x == 3 && y==4){
                cell_data.className = 'black';
            }
            if (x == 4 && y==3){
                cell_data.className = 'black';
            }
            */

            cell.appendChild(cell_data);


            cell.dataset.x = x;
            cell.dataset.y = y;
            // クリックイベントを追加
            cell.addEventListener('click', function() {
                // ここにクリック時の処理を実装
            });
            row.appendChild(cell);
        }
        board.appendChild(row);

        move_posible = [];
        move_posible[19] = 1; 
        move_posible[26] = 1; 
        move_posible[37] = 1; 
        move_posible[44] = 1; 
    }
}


var board_data =[];
var move_posible = [];
var now_turn = true;
var black_num =2;
var white_num =2;
// ページが読み込まれた後にボードを生成
document.addEventListener('DOMContentLoaded', JavascriptInit);