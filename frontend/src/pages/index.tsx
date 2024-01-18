import Layout from '@/components/Shared/Layout'
import {Box, useMediaQuery} from "@chakra-ui/react";



export default function Home() {
    const [mobile] = useMediaQuery('(max-width: 960px)')

    return (
        <Layout breadcrumbs={[]} description='description' title='Меблі, що надихаюь'>
            <Box pos='relative' display='block' mt={mobile ? 4 : 0} pt='32%' bg='brown.100'>
                <Box p={8} position='absolute' top='0'>This is good banner</Box>
            </Box>
        </Layout>
    )
}
