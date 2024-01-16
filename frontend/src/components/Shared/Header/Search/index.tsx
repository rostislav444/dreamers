import {Input, InputGroup, InputLeftElement} from "@chakra-ui/react";
import {SearchIcon} from "@chakra-ui/icons";
import React from "react";


export const Search = () => {
  return <form>
    <InputGroup w={'100%'} h={12}>
      <InputLeftElement pointerEvents="none">
        <SearchIcon w={6} h={6} mt={1.5} ml={3}/>
      </InputLeftElement>
      <Input
        type="search"
        h={'100%'}
        placeholder="Search"
        bg="#7c301110"
        border={'none'}
        color="#7c3011"
        fontSize="20px"
        fontWeight="500"
        pl={12}
        _placeholder={{color: "#7c301180", fontSize: "20px", fontWeight: "500", paddingLeft: "0px"}}
        _focus={{
          boxShadow: "none",
          border: 'none',
          backgroundColor: 'yellow.300',
          borderColor: 'transparent', // Добавьте эту строку

        }}
        // onFocus={(e) => e.target.blur()} // Добавьте эту строку
      />


    </InputGroup>
  </form>
}