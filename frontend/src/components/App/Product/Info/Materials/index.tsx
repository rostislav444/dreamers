import {Box, Flex, Heading, Image, Text, useMediaQuery} from '@chakra-ui/react'
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {InfoHeading} from "@/components/Shared/Typogrphy";
import {useRouter} from 'next/router';
import {ProductPart} from "@/interfaces/Product/Parts";
import {generateMaterialsSlug} from "@/utils/Product/Materials";
import {useState} from "react";
import {ChevronUpIcon} from "@chakra-ui/icons";
import {BASE_URL, MEDIA_LOCAL, MEDIA_URL} from "@/local";
import {log} from 'console';

interface ProductMaterialsInterface {
    parts: ProductPart[]
    selectedMaterials: SelectedMaterialsInterface
    setSelectedMaterials: any
}

export const ProductMaterials = ({parts, selectedMaterials, setSelectedMaterials}: ProductMaterialsInterface) => {
    const router = useRouter()
    const [mobile] = useMediaQuery('(max-width: 960px)');

    // Filter parts with multiple material groups and materials at initialization
    const validParts = parts.filter(part =>
        part.material_groups.length >= 1 &&
        part.material_groups.some(group => group.materials.length > 0)
    );

    const [showAll, setShowAll] = useState<boolean[]>(validParts.map(() => true));

    const handleMaterialsSet = (part: any, groupName: string, material: any) => {
        function addMaterialsToUrl(newMaterials: any) {
            const materialsSlug = Object.values(newMaterials).map((material: any) =>
                material.partId + '-' + material.material
            ).join('_');

            const {slug} = router.query as { slug: string[] };
            const query = {slug: [slug[0], materialsSlug]};

            router.push({
                pathname: router.pathname,
                query: query,
            }, router.pathname, {shallow: true});
        }

        const newMaterials = {
            ...selectedMaterials,
            [part.blender_name]: {
                partId: part.id,
                group: groupName,
                material: material.id,
                material_name: material.name,
            }
        };
        setSelectedMaterials(newMaterials)
        addMaterialsToUrl(newMaterials)
    }


    if (validParts.length === 0) {
        return null;
    }


    return <Box>
        <InfoHeading mobile={mobile}>Колір</InfoHeading>
        {validParts.map((part, i) =>
            <Box key={part.id}>
                <Flex justifyContent='space-between' alignItems='center' onClick={() => setShowAll(old => {
                    const newShowAll = [...old];
                    newShowAll[i] = !old[i];
                    return newShowAll;
                })} mt='2'>
                    <Text fontSize='md'>{part.name}</Text>
                    <ChevronUpIcon w='6' h='6' color='brown.500' cursor='pointer'
                                   transform={showAll[i] ? 'rotate(180deg)' : 'rotate(0deg)'}
                    />
                </Flex>
                {showAll[i] && (<Box>
                    {part.material_groups.map(group =>
                            group.materials.length > 0 && (
                                <Box key={group.id}>
                                    <Text fontSize='sm' mt={1} color={'orange.500'}>{group.name}</Text>
                                    <Box mt={mobile ? 4 : 4} ml={'-5px'} mb={2}>
                                        {group.materials.map(material =>
                                            <Box
                                                key={material.id}
                                                position='relative'
                                                display='inline-block'
                                                m={'0 0 0 2px'}
                                                p='2px'
                                                borderWidth='2px'
                                                borderColor={selectedMaterials[part.blender_name].material === material.id ? 'brown.500' : 'transparent'}
                                                borderRadius='4px'
                                                cursor='pointer'
                                                _hover={{
                                                    borderColor: 'orange.500'
                                                }}
                                                onClick={() => handleMaterialsSet(part, group.name, material)}
                                            >
                                                {material?.material?.color &&
                                                    <Box w={6} h={6} borderRadius='3px' bg={material.material.color.hex}/>}
                                                {material?.material?.image && <Box w={6} h={6}  borderRadius='3px'>
                                                    <Image w='100%' h='100%'
                                                           src={MEDIA_LOCAL ? BASE_URL + material.material.image : material.material.image}
                                                           alt={material.id.toString()}/>
                                                </Box>}
                                            </Box>
                                        )}
                                    </Box>
                                </Box>
                            )
                    )}
                </Box>)}
            </Box>
        )}
    </Box>
}