// Search_Student.js 
// Computer Science 3200 - Assignment 1
// Author(s): Nicholas Jesperson, 201201381

class Search_Student {

    constructor(grid, config) {
        
        this.config = config;       // search configuration object
                                    //   config.actions = array of legal [x, y] actions
                                    //   config.actionCosts[i] = cost of config.actions[i]
                                    //   config.strategy = 'bfs' or 'dfs'

        this.grid = grid;           // the grid we are using to search
        this.sx = -1;               // x location of the start state
        this.sy = -1;               // y location of the start state
        this.gx = -1;               // x location of the goal state
        this.gy = -1;               // y location of the goal state
        this.cost = 0;

        this.inProgress = false;     // whether the search is in progress
        this.strategy = 'bfs';      // the strategy used to do the search
        this.name = 'Student';

        this.path = [];             // the path, if the search found one
        this.open = [];             // the current open list of the search (stores Nodes)
        this.closed = [];           // the current closed list of the search
    
    }
    

    startSearch(sx, sy, gx, gy) {
        this.inProgress = true;     // the search is now considered started
        this.sx = sx;               // set the x,y location of the start state
        this.sy = sy;
        this.gx = gx;               // set the x,y location of the goal state
        this.gy = gy;
        this.path = [];             // set an empty path
        this.open = [];             // set an empty closed and open list
        this.closed = [];
        this.startingNode = new Node(sx, sy, null, null);   //Record where the start and open points are
        this.goalNode = new Node(gx, gy, null, null);
        this.open.push(this.startingNode);                  // Push the start node into the open list
        this.openStates = [];                               //Set open and closed state lists
        this.closedStates = [];
        
        

    }
    /* Fuction gets current grid color and the color of the one that it arrives to after the action.
        Checks to see if the new color is out of bounds. Returns a bool based on its colors */
    isLegalAction(x, y, action) {

        let gridColor = this.grid.get(x,y);
        let action1 = x + action[0];
        let action2 = y + action[1];
        if (this.grid.isOOB(action1, action2,1) == false)
        {
            let newColor = this.grid.get(action1, action2);
            if (gridColor == newColor)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        else {
            return false;
        }
    }

    searchIteration() {
        //Search is finished
        if (this.inProgress == true) {  

        // If open list is empty the cost of the path is -1, and we are finished the search
            if (this.open.length == 0)
            {
                this.inProgress = false;
                this.cost = -1;
            }
            else
            {
                let currentNode = null;
                if (this.config.strategy == "bfs")  //If bfs use a queue
                {
                    currentNode = this.open.shift();
                }
                else if (this.config.strategy == "dfs") //If dfs use a stack
                {
                    currentNode = this.open.pop();
                }
                //Check to see if the current node is the goal node. If it is the search is finished and the path is set
                if (currentNode.x == this.goalNode.x && currentNode.y == this.goalNode.y)
                {
                    this.inProgress = false;
                    while (currentNode.parent !=null)
                    {
                        this.path.push(currentNode.action);
                        currentNode = currentNode.parent;
                    }  
                    this.cost = this.path.length * 100;
                    this.path.reverse();
                }
                var i;
                let statesFound = true;
                //Checks to see if the node x and y is already in the closed states list, if it is continue
                for(i=0; i < this.closedStates.length; i ++)
                {
                    let temp = this.closedStates[i];
                    if(temp[0] == currentNode.x && temp[1] == currentNode.y)
                    {
                        statesFound = false;
                    }
                }
                //If it is not, push it into the closed states list and expand the node.
                if (statesFound)
                {
                    this.closed.push(currentNode);
                    this.closedStates.push([currentNode.x, currentNode.y]);
                    var i;
                    for (i=0; i< this.config.actions.length; i++ )
                    {
                        if (this.isLegalAction(currentNode.x, currentNode.y, this.config.actions[i])) //Each action must be checked to see
                        {                                                                             //if its a legal action
                            let actions = this.config.actions[i];
                            let newX = currentNode.x + actions[0];
                            let newY = currentNode.y + actions[1];
                            let newNode = new Node(currentNode.x + actions[0], currentNode.y + actions[1],actions, currentNode);
                            this.open.push(newNode);                    //Push the new node into the open list and its state into
                            this.openStates.push([newX, newY]);         //open state list.
                                                            
                        }
                    }
                }
            }
        }
    }


    getOpen() {
        return this.openStates;         //Return openStates list
    }


    getClosed() {
        return this.closedStates;       //Returns closedStates list
    }
}

class Node {
    constructor(x, y, action, parent) {
        this.x = x;
        this.y = y;
        this.action = action;
        this.parent = parent;
    }
}