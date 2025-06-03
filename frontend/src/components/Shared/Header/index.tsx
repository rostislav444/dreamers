import React, {useState} from "react";
import {Box, Flex, Grid, Text, useMediaQuery} from "@chakra-ui/react";
import {Burger} from "@/components/Shared/Header/Burger";
import {Search} from "@/components/Shared/Header/Search";
import {Nav} from "@/components/Shared/Header/Nav";
import Link from "next/link";
import dynamic from 'next/dynamic'
import {Logo} from "@/components/Shared/Header/Logo";

const DynamicCartCounter = dynamic(
    () =>
        import('@/components/Shared/Header/Cart').then((module) => module.CartCounter),
    {
        ssr: false,
    }
);

export const Header = () => {
    const [mobile] = useMediaQuery('(max-width: 960px)')
    const [burgerOpen, setBurgerOpen] = useState(false);

    return (
        <Box borderBottom="4px solid" borderBottomColor={'brown.500'}>
            <Grid
                as="header"
                w="calc(100% - 24px)"
                h={mobile ? 16 : 24}
                alignItems='center'
                gap='6'
                templateColumns="auto 32px"
                px={{base: 1, sm: 2, md: 6, lg: 8}}

                m='0 auto'
            >
                <Flex alignItems="center" justifyContent="flex-start">
                    <Burger mobile={mobile} isOpen={burgerOpen} setOpen={setBurgerOpen}/>
                    <Link href={'/'}>
                        <Logo mobile={mobile}/>
                    </Link>
                </Flex>
                {/*<Search/>*/}
                <DynamicCartCounter/>
            </Grid>
            {burgerOpen && <Nav isOpen={burgerOpen} setOpen={setBurgerOpen}/>}
        </Box>
    );
};

export default Header;
