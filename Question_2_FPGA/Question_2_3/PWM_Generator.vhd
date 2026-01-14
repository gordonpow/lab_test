library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity PWM_Generator is
    Port (
        clk     : in  STD_LOGIC;          -- 系統時鐘
        reset   : in  STD_LOGIC;          -- 非同步重設
        input_n : in  unsigned(3 downto 0); -- 輸入值 (1, 2, 3...)
        pwm_out : out STD_LOGIC           -- PWM 輸出信號
    );
end PWM_Generator;

architecture Behavioral of PWM_Generator is
    -- 假設計數器從 0 到 9 (共 10 個階層)
    signal counter : unsigned(3 downto 0) := (others => '0');
begin
    process(clk, reset)
    begin
        if reset = '1' then
            counter <= (others => '0');
            pwm_out <= '0';
        elsif rising_edge(clk) then
            -- 計數器在 0-9 之間循環
            if counter >= 9 then
                counter <= (others => '0');
            else
                counter <= counter + 1;
            end if;

            -- 比較邏輯：當計數器小於輸入值時，輸出高電位
            -- 例如 input_n = 1，則當 counter = 0 時輸出 '1' (占 1/10 = 10%)
            if counter < input_n then
                pwm_out <= '1';
            else
                pwm_out <= '0';
            end if;
        end if;
    end process;
end Behavioral;