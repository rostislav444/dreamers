import {Grid, List, ListItem} from "@chakra-ui/react";
import React, {useState} from "react";
import Link from "next/link";


interface NavItemProps {
  page: {
    name: string;
    link: string;
  }
}

const NavItem = ({page}: NavItemProps) => (
  <ListItem fontSize="24px" fontWeight="500" mb="8px" _hover={{color: "yellow"}}>
    <Link href={page.link}>{page.name}</Link>
  </ListItem>
);

export const Nav = ({isOpen, setOpen}: { isOpen: boolean, setOpen: (isOpen: boolean) => void }) => {
  const [pages] = useState([
    {name: 'Головна', link: '/'},
    {name: 'Каталог', link: '/catalogue'},
  ]);
  return <Grid
    w={80}
    position={'fixed'}
    borderRight="4px solid brown"
    borderBottom="4px solid brown"
    bg={'brown.50'}
    p={2}
    mt={-1}
    zIndex={100}
  >
    <List pl={4} pt={0}>
      {pages.map((page, index) => (
        <NavItem page={page} key={index}/>
      ))}
    </List>
  </Grid>
}