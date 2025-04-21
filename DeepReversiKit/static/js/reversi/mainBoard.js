

class MainBoard{
    constructor(){

        
    }

    //ボードの要素を作成する。
    CreateBoard(){
        const board = document.getElementById('reversi-board');
        for (let y = 0; y < 8; y++) {
            const row = document.createElement('div');
            row.className = 'row';
            for (let x = 0; x < 8; x++) {
                const cell = document.createElement('div');
                cell.className = 'cell';

                const cell_data = document.createElement('div');
                cell_data.className = 'none';

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

        }
    }
    //ボードの更新をする。
    updateBoard(strong_list) {
        if (!strong_list){
            strong_list = [];
        }

        const board = document.getElementById('reversi-board');
        const row = board.getElementsByClassName('row');

        const block_stone_num = document.getElementById('black-count');
        const white_stone_num = document.getElementById('white-count');


        let board_data = mainReversiGame.getBoardIntArray64();
        for (let y = 0; y < 8; y++) {
            
            const cell = row[y].getElementsByClassName('cell');
            for (let x = 0; x < 8; x++) {
                cell[x].removeChild(cell[x].firstChild);

                //まだ子があるなら削除
                if (cell[x].firstChild){
                    cell[x].removeChild(cell[x].firstChild);
                }

            }

            
            for (let x = 0; x < 8; x++) {
                const cell_data = document.createElement('div');
                cell_data.className = 'none';

                if (board_data[x+y*8]==-1){
                    cell_data.className = 'black stone';
                }
                if (board_data[x+y*8]==1){
                    cell_data.className = 'white stone';
                }
                if (mainReversiGame.possible_move_array[y*8+x]){
                    cell_data.className = 'possible';
                }

                cell[x].appendChild(cell_data);

                if (strong_list.includes(x+y*8)){
                    const cell_data2 = document.createElement('div');
                    cell_data2.className = 'strong';
                    cell[x].appendChild(cell_data2);

                }
            }
        }

        let color = "";
        if (now_turn){
            color = "黒";
        }else{
            color = "白";
        }
        //document.getElementById('now-turn').textContent = color;


        //block_stone_num.textContent =""+black_num;
        //white_stone_num.textContent =""+white_num;
    }


}

