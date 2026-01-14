library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_Random_Gen is
-- Testbench 不需要 Port
end tb_Random_Gen;

architecture sim of tb_Random_Gen is
    -- 宣告與元件相同的訊號
    signal clk      : std_logic := '0';
    signal reset    : std_logic := '0';
    signal input_en : std_logic := '0';
    signal rand_out : std_logic_vector(1 downto 0);

    -- 定義時鐘週期 (10ns = 100MHz)
    constant clk_period : time := 10 ns;

begin
    -- 實例化被測元件 (UUT)
    uut: entity work.Random_Gen_0to3
        port map (
            clk      => clk,
            reset    => reset,
            input_en => input_en,
            rand_out => rand_out
        );

    -- 【修改部分】無限循環的時鐘產生過程
    clk_process : process
    begin
        clk <= '0';
        wait for clk_period / 2;
        clk <= '1';
        wait for clk_period / 2;
        -- 這裡不需要 loop，process 本身執行完就會從頭開始，達成無限 CLK
    end process;

    -- 刺激過程 (Stimulus process)
    stim_proc: process
    begin		
        -- 1. 系統重置
        reset <= '0';
        wait for 22 ns; -- 稍微偏移，避開上升沿以確保訊號穩定
        reset <= '1';
        wait for clk_period;

        -- 2. 設定輸入為 1，開始生成隨機數
        input_en <= '1';
        
        -- 持續一段時間以產生連續隨機數
        -- 若要在模擬器看到結果，請手動設定模擬執行時間 (如 run 1us)
        wait for clk_period * 10; 

        -- 3. 停止生成
        input_en <= '0';
        
        -- 模擬將會在這裡持續掛起，但 clk_process 會在背景一直跳動
        wait; 
    end process;

end sim;