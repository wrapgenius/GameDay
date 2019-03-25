from numpy import np
from pandas import pd

class Draft:
    
    def __init__(self, projection, number_teams = 12,
                 batters  = {'C','1B','2B', '3B','SS','OF','UTIL'},
                 pitchers = {'SP','RP','P'},
                 number_positions = {'C':1,'1B':1,'2B':1, '3B':1,'SS':1,'OF':3,'UTIL':1,'SP':2,'RP':2,'P':3,'BN':5}, 
                 batter_statline  = {'R':0,'1B':0,'2B':0, '3B':0,'HR':0,'RBI':0,'SB':0,'BB':0,'AVG':0,'OPS':0}, 
                 pitcher_statline = {'W':0, 'L':0,'CG':0,'SHO':0,'SV':0,'BB':0,'SO':0,'ERA':0,'WHIP':0,'BSV':0} ):
        
        self.projection = projection
        self.batters  = batters
        self.pitchers = pitchers
        self.open_positions = number_positions
        self.batter_statline = batter_statline
        self.pitcher_statline = pitcher_statline        
        self.number_teams = number_teams

        bat_rows = []
        bat_cols = ['Name']
        for ibat in self.batters:
            for i in range(self.open_positions[ibat]):
                bat_rows.append(ibat)
        for ibat in self.batter_statline:
            bat_cols.append(ibat)
        print(bat_rows)        
        print(bat_cols)
        
        bat_df = pd.DataFrame(np.zeros([len(bat_rows),len(bat_cols)]), columns = bat_cols)
        bat_df['Position'] = bat_rows
        
        pit_rows = ['Name']
        pit_cols = []
        for ipit in self.pitchers:
            for i in range(self.open_positions[ipit]):
                pit_rows.append(ipit)
        for ipit in self.pitcher_statline:
            pit_cols.append(ipit)
            
        print(pit_rows)        
        print(pit_cols)
        
        pit_df = pd.DataFrame(np.zeros([len(pit_rows),len(pit_cols)]), columns = pit_cols)
        pit_df['Position'] = pit_rows   
        
        self.bat_df = bat_df
        self.pit_df = pit_df
        
        #return bat_df, pit_df
    
    def draft_team(self, draft_position = 'Best'):
        print(self.number_teams)
        self.draftees  = pd.DataFrame()
        for psn in self.batters:
            print(psn)
            if psn != 'UTIL':
                #print(psn)
                ranked_position_df = self.projection.statline['batters'][(self.projection.statline['batters']['Position']==psn) & (self.projection.statline['batters']['Drafted']==False)].sort_values('Rank')[0:self.number_teams]
                rank_stat = np.zeros([len(self.batter_statline),self.number_teams])

                for i in range(len(self.batter_statline)):
                    cat = self.batter_statline.keys()[i]
                    #print(cat)
                    ind = np.argsort(ranked_position_df[cat])
                    if cat in ['HR', 'R', 'RBI', '2B', 'SB', '1B', '3B', 'BB', 'AVG', 'OPS']:
                        rank_stat[i, ind[::-1]]= np.arange(len(ind),0,-1)
                position_rank = np.sum(rank_stat.T, axis=1)
                print(position_rank)

                #for i in (1 + np.arange(self.number_teams - 1)):
                #    print(-i)
                #    print(psn,ranked_position_df.Name.values[np.argsort(position_rank)[-i]], np.sort(position_rank)[-i])
                print(psn,ranked_position_df.Name.values[np.argsort(position_rank)[-1]], np.sort(position_rank)[-1])
                
                df = pd.DataFrame([psn,ranked_position_df.Name.values[np.argsort(position_rank)[-1]], np.sort(position_rank)[-1]])
                if self.draftees.empty:
                    self.draftees = df.T
                else:
                    self.draftees = pd.concat([self.draftees, df.T])
                
        for psn in self.pitchers:
            if psn != 'P':
                ranked_position_df = self.projection.statline['pitchers'][(self.projection.statline['pitchers']['Position']==psn) & (self.projection.statline['pitchers']['Drafted']==False)].sort_values('Rank')[0:self.number_teams]
                rank_stat = np.zeros([len(self.pitcher_statline),self.number_teams])

                for i in range(len(self.pitcher_statline)):
                    cat = self.pitcher_statline.keys()[i]
                    #print(cat)
                    ind = np.argsort(ranked_position_df[cat])
                    if cat in ['SO', 'W', 'SV', 'ERA', 'CG', 'SHO']:
                        rank_stat[i, ind[::-1]]= np.arange(len(ind),0,-1)
                    else:
                        rank_stat[i, ind]= np.arange(len(ind),0,-1)
                position_rank = np.sum(rank_stat.T, axis=1)
                #for i in (1 + np.arange(self.number_teams - 1)):
                #    print(psn,ranked_position_df.Name.values[np.argsort(position_rank)[-i]], np.sort(position_rank)[-i])

                print(psn,ranked_position_df.Name.values[np.argsort(position_rank)[-1]], np.sort(position_rank)[-1])
                
                df = pd.DataFrame([psn,ranked_position_df.Name.values[np.argsort(position_rank)[-1]], np.sort(position_rank)[-1]])
                self.draftees = pd.concat([self.draftees, df.T])
                
