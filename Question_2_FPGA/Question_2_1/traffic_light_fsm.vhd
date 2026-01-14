library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity traffic_light_fsm is
    Port ( 
        clk   : in  STD_LOGIC;
        rst_n : in  STD_LOGIC; -- 非同步低電位重置
        light : out STD_LOGIC_VECTOR (2 downto 0) -- [紅, 黃, 綠]
    );
end traffic_light_fsm;

architecture Behavioral of traffic_light_fsm is
    -- 定義狀態類型
    type state_type is (S_GREEN, S_YELLOW, S_RED);
    signal current_state : state_type;
    
    -- 計數器，足以計數到 10 (0 to 15)
    signal timer : unsigned(3 downto 0);

begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            current_state <= S_GREEN;
            timer <= (others => '0');
            light <= "001"; -- 初始為綠燈
            
        elsif falling_edge(clk) then
            case current_state is
                
                when S_GREEN =>
                    light <= "001";
                    if timer < 6 then  -- 持續 8 個 clks (0-7)
                        timer <= timer + 1;
                    else
                        timer <= (others => '0');
                        current_state <= S_YELLOW;
                    end if;

                when S_YELLOW =>
                    light <= "010";
                    if timer <= 1 then  -- 持續 2 個 clks (0-1)
                        timer <= timer + 1;
                    else
                        timer <= (others => '0');
                        current_state <= S_RED;
                    end if;

                when S_RED =>
                    light <= "100";
                    if timer < 9 then  -- 持續 10 個 clks (0-9)
                        timer <= timer + 1;
                    else
                        timer <= (others => '0');
                        current_state <= S_GREEN;
                    end if;

                when others =>
                    current_state <= S_GREEN;
            end case;
        end if;
    end process;

end Behavioral;