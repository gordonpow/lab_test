library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity traffic_light_fsm_tb is
-- Testbench 不需要埠號 (Ports)
end traffic_light_fsm_tb;

architecture sim of traffic_light_fsm_tb is

    -- 宣告待測元件 (UUT)
    component traffic_light_fsm
        Port ( 
            clk   : in  STD_LOGIC;
            rst_n : in  STD_LOGIC;
            light : out STD_LOGIC_VECTOR (2 downto 0)
        );
    end component;

    -- 內部訊號宣告
    signal clk   : STD_LOGIC := '0';
    signal rst_n : STD_LOGIC := '0';
    signal light : STD_LOGIC_VECTOR (2 downto 0);

    -- 時脈週期定義 (10ns = 100MHz)
    constant clk_period : time := 10 ns;

begin

    -- 實體化待測元件 (Unit Under Test)
    uut: traffic_light_fsm Port map (
          clk   => clk,
          rst_n => rst_n,
          light => light
        );

    -- 時脈產生程序
    clk_process : process
    begin
        while now < 500 ns loop -- 模擬執行 500ns 後停止
            clk <= '0';
            wait for clk_period/2;
            clk <= '1';
            wait for clk_period/2;
        end loop;
        wait;
    end process;

    -- 測試激勵程序 (Stimulus Process)
    stim_proc: process
    begin		
        -- 初始狀態：重置系統
        rst_n <= '0';
        wait for 20 ns;	
        
        rst_n <= '1'; -- 釋放重置，開始運作
        
        -- 觀察波形轉換
        -- 綠燈應持續 80ns (8 clks * 10ns)
        -- 黃燈應持續 20ns (2 clks * 10ns)
        -- 紅燈應持續 100ns (10 clks * 10ns)
        
        wait;
    end process;

end sim;