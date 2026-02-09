import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Box } from "@mui/material";

export default function ChatMarkdown({ content }) {
  return (
    <Box
      sx={{
        fontSize: 14,
        lineHeight: 1.6,

        "& p": { margin: 0 },
        "& ul": { paddingLeft: 3, margin: 0 },
        "& ol": { paddingLeft: 3, margin: 0 },
        "& li": { margin: 0 },
        "& strong": { fontWeight: 700 },
      }}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
      >
        {content}
      </ReactMarkdown>
    </Box>
  );
}
