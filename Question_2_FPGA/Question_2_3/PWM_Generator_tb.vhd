library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity PWM_Generator_tb is
-- Testbench 不需要 Port
end PWM_Generator_tb;

architecture sim of PWM_Generator_tb is
    -- 宣告與元件相同的訊號
    signal clk     : std_logic := '0';
    signal reset   : std_logic := '0';
    signal input_n : unsigned(3 downto 0) := (others => '0');
    signal pwm_out : std_logic;

    -- 定義時鐘週期 (例如 100MHz = 10ns)
    constant clk_period : time := 10 ns;

begin
    -- 實例化被測元件 (UUT)
    uut: entity work.PWM_Generator
        port map (
            clk     => clk,
            reset   => reset,
            input_n => input_n,
            pwm_out => pwm_out
        );

    -- 時鐘產生過程
    clk_process : process
    begin
        while now < 1000 ns loop  -- 總共模擬 1000ns
            clk <= '0';
            wait for clk_period / 2;
            clk <= '1';
            wait for clk_period / 2;
        end loop;
        wait;
    end process;

    -- 刺激過程 (Stimulus process)
    stim_proc: process
    begin		
        -- 1. 初始化與重設
        reset <= '1';
        wait for 20 ns;
        reset <= '0';

        -- 2. 測試 10% 占空比 (Input = 1)
        input_n <= "0001";
        wait for 150 ns;

        -- 3. 測試 20% 占空比 (Input = 2)
        input_n <= "0010";
        wait for 150 ns;

        -- 4. 測試 50% 占空比 (Input = 5)
        input_n <= "0101";
        wait for 150 ns;

        -- 停止模擬
        wait;
    end process;

end sim;