import React, {useEffect, useState} from 'react';

const plot_desc = {
    'elo_rating': "This plot shows an interesting way of looking at a player's elo rating over time.\
    I think it is more enlightening than the basic elo plots on chess.com, here we see ‘nodes’ or\
    circular regions where a player has spent time for a given elo space.\
    It is cool to see how the nodes slowly progress from low 800 to higher ranges like 1400 if you are like me.",
    'match_wins': "This plot is very simple, but it is useful for players, especially those just starting out. In theory a player should be close to 50-50 on either black or white, but as we see sometimes you win a lot more as white and other times as black. In my case early on I had a strong opening as white which I learned to play well, but I lacked as black to have a strong defensive opening. Then I learned the famous Caro-Kann defense as black and then that became my stronger side, and I won significantly more as black than as white in my higher elo matches.",
    'openings': `This plot was me applying a tree data structure which I was learning about to my own chess matches. I have not seen a plot liek this anywhere but I found it very insightful. It is a tree structure over all my games starting with the opening move to the n-th move (defaults to 2 because it gets crazy to view). In chess usually the first few moves you make determine a lot of what happens in the game so just viewing the tree for the first 2-3 moves is very helpful. At the end node of each branch there is a number which is the times that mainline has been played in your games.

        This can be helpful to track what type of games you play a lot and which you play less.`,
        }


function DashBoard({plotData}) {
    const [option,setOption] = useState('')

    useEffect(() => {
        setOption(plotData.selectedOption)
    },[plotData]
    );

    return (
        <div>     
            <div className="dashboard">
                <h1>DashBoard</h1>
                {
                option === 'Option 1' ? plot_desc.elo_rating :
                option === 'Option 2' ? plot_desc.match_wins :
                option === 'Option 3' ? plot_desc.openings :
                <text>Hi, welcome to ChessViz. I made this to help visualize my chess games over the years. I wanted 
                    more in depth data anlysis tools to see what I can learn from my macthes to improve and also see my progress.
                </text>}
            </div>
        </div>
    )
}

export default DashBoard