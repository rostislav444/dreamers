import React from 'react'
import Head from 'next/head'
import {Header} from "@/components/Shared/Header";
import Link from 'next/link'

import {Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink, useMediaQuery,} from "@chakra-ui/react";
import {Footer} from "@/components/Shared/Footer";

interface Breadcrumb {
    title: string;
    link?: string;
}

interface LayoutProps {
    children: React.ReactNode;
    title: string;
    description: string;
    breadcrumbs: Breadcrumb[];
    isHomePage?: boolean;
}

export default function Layout({children, title, description, breadcrumbs, isHomePage = false}: LayoutProps) {
    const [mobile] = useMediaQuery('(max-width: 960px)')
    const fullBreadcrumbs = [
        {title: 'Головна', link: '/'},
        ...breadcrumbs
    ]

    return (
        <>
            <Head>
                <title>{`Dreamers ✨${title || ''}`}</title>
                <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no"/>
                {description && <meta name="description" content={description}/>}
            </Head>
            <Box>
                <Header/>
                <Box
                    as='main'
                    w={isHomePage ? '100%' : 'calc(100% - 24px)'}
                    minH='calc(100vh - 700px)'
                    px={isHomePage ? 0 : {base: 1, sm: 2, md: 6, lg: 8}}
                    py={isHomePage ? 0 : {base: 2, sm: 4, md: 6, lg: 8}}
                    m={isHomePage ? 0 : '0 12px'}
                >
                    {breadcrumbs.length > 0 && <Breadcrumb
                        mt={4}
                        mb={8}
                        fontWeight={500}
                        separator='>'
                        overflowX='auto'
                    >
                        {fullBreadcrumbs.map((breadcrumb, index) => (
                            <BreadcrumbItem whiteSpace={'nowrap'} key={index}
                                            isCurrentPage={breadcrumb.link === undefined}>
                                {breadcrumb.link ?
                                    <BreadcrumbLink as={Link}
                                                    href={breadcrumb.link}>{breadcrumb.title}</BreadcrumbLink>
                                    : <span>{breadcrumb.title}</span>
                                }
                            </BreadcrumbItem>
                        ))}
                    </Breadcrumb>}
                    {children}
                </Box>
            </Box>
            <Footer/>
        </>
    )
}