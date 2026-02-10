import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Box } from "@mui/material";
import { memo } from "react";

function ChatMarkdown({ content }) {
  return (
    <Box
      sx={{
        fontSize: 16,
        lineHeight: 1.5,
        color: "text.primary",
        "& p": {
          margin: 0,
          marginBottom: 1
        },
        "& h1, & h2, & h3, & h4, & h5, & h6": {
          margin: 0,
          marginTop: 1.5,
          marginBottom: 0.5,
          fontWeight: 600,
        },

        "& ul, & ol": { paddingLeft: 3, margin: 0, marginBottom: 1 },
        "& li": { marginBottom: 0.5 },
        "& > *:last-child": {
          marginBottom: 0
        },

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

export default memo(ChatMarkdown);
