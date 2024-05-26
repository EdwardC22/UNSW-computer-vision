import { MoonIcon, SunIcon } from "@chakra-ui/icons";
import { IconButton, useColorMode } from "@chakra-ui/react";
import * as React from "react";

// Alter colour theme between dark and light

const ThemeToggle = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <>
      <IconButton
        icon={colorMode === "light" ? <MoonIcon /> : <SunIcon />}
        aria-label="Toggle colour theme"
        onClick={toggleColorMode}
      />
    </>
  );
};

export default ThemeToggle;
