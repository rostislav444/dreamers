import {Box, Flex, Heading, Image, Text, useMediaQuery} from '@chakra-ui/react'
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {InfoHeading} from "@/components/Shared/Typogrphy";
import {useRouter} from 'next/router';
import {ProductPart} from "@/interfaces/Product/Parts";
import {generateMaterialsSlug} from "@/utils/Product/Materials";
import {useState} from "react";
import {ChevronUpIcon} from "@chakra-ui/icons";
import {BASE_URL, MEDIA_LOCAL, MEDIA_URL} from "@/local";

interface ProductMaterialsInterface {
    parts: ProductPart[]
    selectedMaterials: SelectedMaterialsInterface
    setSelectedMaterials: any
}

export const ProductMaterials = ({parts, selectedMaterials, setSelectedMaterials}: ProductMaterialsInterface) => {
    const router = useRouter()
    const [mobile] = useMediaQuery('(max-width: 960px)');
    const [showAll, setShowAll] = useState<boolean[]>(parts.map((_, i) => i === 0));

    const handleMaterialsSet = (partId: number, materialId: number) => {
        const newMaterials = {...selectedMaterials, [partId]: materialId};
        setSelectedMaterials(newMaterials);

        const materialsSlug = generateMaterialsSlug(newMaterials);
        const {slug} = router.query as { slug: string[] };
        const query = {slug: [slug[0], materialsSlug]};

        router.push({
            pathname: router.pathname,
            query: query,
        }, router.pathname, {shallow: true});

    }

    return <Box>
        <InfoHeading mobile={mobile}>Колір</InfoHeading>
        {parts.map((part, i) =>
            <Box key={part.id}>
                <Flex justifyContent='space-between' alignItems='center' onClick={() => setShowAll(old => {
                    const newShowAll = [...old];
                    newShowAll[i] = !old[i];
                    return newShowAll;
                })} mt='4'>
                    <Text fontSize='md'>{part.name}</Text>
                    <ChevronUpIcon w='6' h='6' color='brown.500' cursor='pointer'
                                   transform={showAll[i] ? 'rotate(180deg)' : 'rotate(0deg)'}
                    />
                </Flex>
                {showAll[i] && (<Box>
                    {part.material_groups.map(group =>
                        <Box key={group.id}>
                            <Text fontSize='sm' mt={1} color={'orange.500'}>{group.name}</Text>
                            <Box mt={mobile ? 4 : 4} ml={'-9px'} mb={mobile ? 4 : 6}>
                                {group.materials.map(material =>
                                    <Box
                                        key={material.id}
                                        position='relative'
                                        display='inline-block'
                                        m={'0 0 0 2px'}
                                        p='2px'
                                        borderWidth='2px'
                                        borderColor={selectedMaterials[part.id] === material.id ? 'brown.500' : 'transparent'}
                                        borderRadius='0'
                                        cursor='pointer'
                                        _hover={{
                                            borderColor: 'orange.500'
                                        }}
                                        onClick={() => handleMaterialsSet(part.id, material.id)}
                                    >
                                        {material.color && <Box w={6} h={6} bg={material.color.hex}/>}
                                        {material.material && <Box w={6} h={6}>
                                            <Image w='100%' h='100%'
                                                   src={MEDIA_LOCAL ? BASE_URL + material.material.image : material.material.image}
                                                   alt={material.id.toString()}/>
                                        </Box>}
                                    </Box>
                                )}
                            </Box>
                        </Box>
                    )}
                </Box>)}
                {}
            </Box>
        )
        }
    </Box>
}