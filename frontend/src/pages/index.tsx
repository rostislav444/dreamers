import NextLink from 'next/link'
import Layout from '@/components/Shared/Layout'
import {Box} from "@chakra-ui/react";



export default function Home() {
    return (
        <Layout breadcrumbs={[]} description='description' title='title'>
            <Box pos='relative' display='block' pt='32%' bg='brown.100'>
                <Box p={8} position='absolute' top='0'>This is good banner</Box>
            </Box>
        </Layout>
    )
}
