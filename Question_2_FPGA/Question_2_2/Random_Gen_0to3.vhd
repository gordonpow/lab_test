library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Random_Gen_0to3 is
    Port (
        clk      : in  STD_LOGIC;
        reset    : in  STD_LOGIC;
        input_en : in  STD_LOGIC;
        rand_out : out STD_LOGIC_VECTOR(1 downto 0) -- 題目要求輸出 q[0]，這裡取兩位做 0-3
    );
end Random_Gen_0to3;

architecture Behavioral of Random_Gen_0to3 is
    -- 根據圖片題目：初始值為 11110
    signal q : std_logic_vector(4 downto 0) := "11110"; 
begin
    process(clk, reset)
    begin
        if reset = '0' then
            q <= "11110"; -- 題目要求的 Reset 值
        elsif falling_edge(clk) then
            if input_en = '1' then
                q(4) <= q(0) xor '0';      -- 最左邊的 XOR (接 0)
                q(3) <= q(4);              -- 直接移位
                q(2) <= q(3) xor q(0);     -- 中間的 XOR (q[3] xor q[0])
                q(1) <= q(2);              -- 直接移位
                q(0) <= q(1);              -- 直接移位
            end if;
        end if;
    end process;

    -- 輸出映射：題目說輸出在 q[0]，若要生成 0-3，我們取 q(1 downto 0)
    rand_out <= q(1 downto 0);
end Behavioral;