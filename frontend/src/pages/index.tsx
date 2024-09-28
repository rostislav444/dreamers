import Layout from '@/components/Shared/Layout'
import {Box, Grid, GridItem, useMediaQuery} from "@chakra-ui/react";
import fetchApi from "@/utils/fetch";
import type {GetStaticProps} from "next";
import Link from "next/link";


interface Props {
    categories: any
}


export default function Home({categories}: Props) {
    const [mobile] = useMediaQuery('(max-width: 960px)')

    return (
        <Layout breadcrumbs={[]} description='description' title='Меблі, що надихаюь'>
            <Grid gridTemplateColumns='repeat(auto-fill, minmax(200px, 1fr))' gap={4}>
                {categories.map((category: any) => (
                    <GridItem key={category.id} colSpan={mobile ? 1 : 2}>
                        <Link href='/catalogue/[slug]' as={`/catalogue/${category.slug}`}>
                            <Box bg='brown.100' p={4} _hover={{bg: 'brown.500', color: 'yellow.200'}}>
                                <h3>{category.name}</h3>
                            </Box>
                        </Link>
                    </GridItem>
                ))}
            </Grid>
        </Layout>
    )
}


export const getStaticProps = (async (context) => {
    const api = fetchApi()
    const categoriesResp = await api.get('category');


    return {
        props: {
            categories: categoriesResp.ok ? categoriesResp.data : []
        },
        revalidate: 60 * 5,
    }

}) satisfies GetStaticProps<{ categories: any }>
