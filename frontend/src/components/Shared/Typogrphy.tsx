import {Heading} from "@chakra-ui/react";


export const InfoHeading = ({children, mobile}: { children: string, mobile?: boolean }) => <Heading
    mt={mobile ? 4 : 6}
    mb={mobile ? 4 : 5}
    size='md'
    pb={mobile ? 4 : 6}
    borderBottomColor='brown.500'
    color='brown.500'
    borderBottomWidth='3px'>
    {children}
</Heading>
